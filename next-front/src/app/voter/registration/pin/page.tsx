"use client"

import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { z } from "zod"
import { Button } from "@/components/ui/button"
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { useRouter } from "next/navigation"


const BACKEND_URL = "http://localhost:8000";

const formSchema = z.object({
  PINcode: z.string().min(2, {
    message: "Username must be at least 2 characters.",
  }),
})

const PINpage = () => {
  const router = useRouter();
  
  // 1. Define your form.
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      PINcode: "",
    },
  })

  // 2. Define a submit handler.
  async function onSubmit(values: z.infer<typeof formSchema>) {
    // Do something with the form values.
    // ✅ This will be type-safe and validated.
    try{
        const registrationData = sessionStorage.getItem("registrationData");
        if (!registrationData) {
            throw new Error("No");
        }

        const parseData = JSON.parse(registrationData);
        const requestData = { ...parseData, PINcode: Number(values.PINcode)}
        requestData.Age = Number(requestData.Age);
        console.log(requestData)
        console.log(registrationData);

        const response = await fetch(BACKEND_URL+"/registration/regist_pin",{
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
        if(data.status === "success") {
            console.log("pin success");
            return (
                <h1>your PINcode has been saved</h1>
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
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
        <FormField
          control={form.control}
          name="PINcode"
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
  )
}


export default PINpage