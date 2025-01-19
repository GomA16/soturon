"use client"

import { BACKEND_URL } from "@/src/config/constants";
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
  async function onSubmit(values: z.infer<typeof formSchema>) {
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
        const ciphers = [encPIN.ctxt[0].toString(), encPIN.ctxt[1].toString()];
        // const pk = new ElgamalPlainText(bigInt(electionData.voterInfoList[0].verifyKey));
        // const encPk = new ElgamalCipherText();
        // encPk.encryption(params, keys, pk);

        const requestData = {"pk":electionData.voterInfoList[0].verifyKey , "PIN": ciphers};
        sessionStorage.setItem("pinData", JSON.stringify(requestData));
        console.log("requestData",requestData);

        const response = await fetch(BACKEND_URL+"/registration/registerPIN",{
                method:"POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(requestData),
            }
        );

        if (!response.ok) {
            throw new Error("era-dayo");
        }

        const data = await response.json();
        console.log("data", data);
        if(data.status === "success") {
            console.log("pin success");
            return (
                router.push("/voter/registration/complete")
            );
        }else{
            console.log("pin failed");
            return (
                <h1>you have already registared your PIN code</h1>
            )
        }
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