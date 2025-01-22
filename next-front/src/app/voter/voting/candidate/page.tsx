"use client"

import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { z } from "zod"
import { Button } from "@/components/ui/button"
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { useEffect, useState } from "react"
import { BACKEND_URL } from "@/src/config/constants"
import { ElgamalCipherText, ElgamalKeys, ElgamalPlainText, Parameters } from "@/src/app/tools/myPrimitives/elgamal"
import electionData from "@/data/electionData.json"
import bigInt from "big-integer"
import { useRouter } from "next/navigation"

interface Candidate {
  index: string;
  name: string;
  party: string;
  district: string;
};

const SelectCandidate = () => {
  const router = useRouter();
  const [radioOptions, setRadioOptions] = useState<Candidate[]>([]);  // APIから取得したラジオボタンの選択肢を格納する状態
  const [schemaValue, setSchemaValue] = useState<string[]>([]);
    // フォームのスキーマ
    const FormSchema = z.object({
        type: z.string().refine(value => {
            return schemaValue.includes(value); // validValuesがAPIから取得した選択肢
        }, {
            message: "Invalid selection, please choose a valid option.",
        }),
    })
    const form = useForm<z.infer<typeof FormSchema>>({
      resolver: zodResolver(FormSchema),
    });
  useEffect(() => {
    // APIを叩いて選択肢を取得
    const fetchOptions = async () => {
      try {
        const response = await fetch(BACKEND_URL + "/voting/getCandidateList");  // 適切なAPIエンドポイントに変更
        if (!response.ok) {
          throw new Error("Failed to fetch options");
        }
        const data = await response.json();
        console.log(data.candidateList);
        const values = data.candidateList.map((candidate:Candidate) => candidate.index);
        setRadioOptions(data.candidateList);  // 取得したデータを状態にセット
        console.log(values)
        setSchemaValue(values);
        console.log(radioOptions);
      } catch (error) {
        console.error("Error fetching options:", error);
      }
    }

    fetchOptions();
  }, [radioOptions]);

  function onSubmit(data: z.infer<typeof FormSchema>) {
    const params = new Parameters();
    params.setParams(electionData.election_vars.parameters);
    const keys = new ElgamalKeys();
    keys.setKeys(electionData.election_vars.tallyKeys);
    const candidate = new ElgamalPlainText(bigInt(data.type));
    const encCandidate = new ElgamalCipherText();
    encCandidate.encryption(params, keys, candidate);
    sessionStorage.setItem("encCandidate", JSON.stringify({encCandidate: encCandidate}));
    router.push("/voter/voting/pin");
    console.log(encCandidate);
  }

  return (
    <div className="h-screen flex justify-center items-center" style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="w-2/3 space-y-6">
          <FormField
            control={form.control}
            name="type"
            render={({ field }) => (
              <FormItem className="space-y-3">
                <FormLabel>Notify me about...</FormLabel>
                <FormControl>
                  <RadioGroup
                    onValueChange={field.onChange}
                    defaultValue={field.value}
                    className="flex flex-col space-y-3"
                  >
                    {/* ラジオボタンの選択肢がAPIから取得されるまで、ローディング中の表示 */}
                    {radioOptions.length === 0 ? (
                      <p>Loading options...</p>
                    ) : (
                      radioOptions.map((option: Candidate) => (
                        <FormItem key={option.index} className="flex items-center space-x-3 space-y-0">
                          <FormControl>
                            <RadioGroupItem value={option.index} />
                          </FormControl>
                          <FormLabel className="font-normal">{option.name}</FormLabel>
                        </FormItem>
                      ))
                    )}
                  </RadioGroup>
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <Button type="submit">Submit</Button>
        </form>
      </Form>
    </div>
  )
}

export default SelectCandidate;