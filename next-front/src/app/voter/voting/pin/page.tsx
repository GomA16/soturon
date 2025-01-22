"use client"

import electionData from "@/data/electionData.json";
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
import { Input } from "@/components/ui/input"
import { ElgamalCipherText, ElgamalKeys, ElgamalPlainText, Parameters } from "@/src/app/tools/myPrimitives/elgamal";
import bigInt from "big-integer";
import { useRouter } from "next/navigation";



const formSchema = z.object({
    PIN: z.string().min(2, {
    message: "Username must be at least 2 characters.",
  }),
})

const PINpage = () => {
  const router = useRouter();
  
  // 1. Define your form.
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      PIN: "",
    },
  })

  // 2. Define a submit handler.
  function onSubmit(values: z.infer<typeof formSchema>) {
    // Do something with the form values.
    // ✅ This will be type-safe and validated.
    try{
        // PINの暗号化
        const params = new Parameters();
        params.setParams(electionData.election_vars.parameters);
        const keys = new ElgamalKeys();
        keys.setKeys(electionData.election_vars.authKeys);
        const pin = new ElgamalPlainText(bigInt(values.PIN));
        const encPIN = new ElgamalCipherText();
        encPIN.encryption(params,keys,pin);
        // const ciphers = {
        //     c1: encPIN.ctxt[0].toString(), 
        //     c2: encPIN.ctxt[1].toString()
        // };
        const storageData = sessionStorage.getItem("encCandidate");
        let encCandidate;
        if (typeof(storageData) == "string"){
          encCandidate = JSON.parse(storageData).encCandidate;
        }
        const ballot = {
            pk: electionData.voterInfoList[0].verifyKey,
            pin: encPIN.ctxt,
            candidate: encCandidate.ctxt
        };
        // sessionStorage.setItem("encPIN", JSON.stringify(ciphers));
        sessionStorage.setItem("ballot", JSON.stringify(ballot));
        router.push("/voter/voting/checkinfo");
    }catch(error){
        console.log("pin code error", error)
    }
    console.log(values)
  }

  return (

    <div className="h-screen flex justify-center items-center"
    style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
          <FormField
            control={form.control}
            name="PIN"
            render={({ field }) => (
              <FormItem>
                <FormLabel>PIN code</FormLabel>
                <FormControl>
                  <Input placeholder="input PIN code" {...field} />
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


export default PINpage