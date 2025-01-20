"use client";

import { Button } from "@/components/ui/button";
import { genSignature, getChallenge, sendResponse } from "@/src/app/components/authentication";
import React, {useEffect, useState} from "react";
import electionData from "@/data/electionData.json";
import  Link  from "next/link";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input"
import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { z } from "zod"


const VotingTop = () => {
    const formSchema = z.object({
        id: z.string().min(1, {
        message: "id must be at least 2 characters.",
      }),
    })
    const [status, setStatus] = useState("loading...");
    // const router = useRouter();
    
    // 1. Define your form.
    const form = useForm<z.infer<typeof formSchema>>({
      resolver: zodResolver(formSchema),
      defaultValues: {
        id: "",
      },
    })

    const saveData = (voterData: any):boolean => {
        sessionStorage.setItem("voterData", JSON.stringify({voterData}));
        return true
    };

    // const handleProcess = async () => {
        
    //     // いったんjsonからデータを読み出す
    //     const voterList = electionData.voterInfoList;
    //     const voter = voterList[0];
    //     console.log("voter", voter);
    
    //     // 署名の生成
    //     const signKey = voter.signKey;
    
    //     // レスポンス生成
    //     const challenge = await getChallenge();
    //     if (!challenge) {
    //         console.log("Failed to get challenge");
    //         return;
    //     }

    //     const message: string = Buffer.from(challenge.toString()).toString("base64");
    //     const signature = await genSignature(message, signKey);
    //     if (!signature) {
    //         console.log("Failed to generate signature");
    //         return;
    //     }
    //     const voterData = {
    //         "name":voter.name,
    //         "Age":voter.Age,
    //         "Gender":voter.Gender,
    //         "pk": voter.verifyKey,
    //         "challenge": message,
    //         "signature": signature
    //     };
    //     const isSuccess = await sendResponse(voterData, '/voting/verifyVoter');
    //     if (isSuccess) {
    //         setStatus("Success!");
    //         console.log("Voter registration successful!");
    //     } else {
    //         setStatus("Failed");
    //         console.log("Voter registration failed.");
    //     }
    //     saveData(voterData);
    // };

    // useEffect(() => {handleProcess()}, []);

    const onSubmit = async(values: z.infer<typeof formSchema>) => {
        
        // いったんjsonからデータを読み出す->最終的にはデータベースから読み出す
        const voterList = electionData.voterInfoList;
        const voter = voterList[Number(values.id)];
        console.log("voter", voter);
    
        // 署名の生成
        const signKey = voter.signKey;
    
        // レスポンス生成
        const challenge = await getChallenge();
        if (!challenge) {
            console.log("Failed to get challenge");
            return;
        }

        const message: string = Buffer.from(challenge.toString()).toString("base64");
        const signature = await genSignature(message, signKey);
        if (!signature) {
            console.log("Failed to generate signature");
            return;
        }
        const voterData = {
            "name":voter.name,
            "Age":voter.Age,
            "Gender":voter.Gender,
            "pk": voter.verifyKey,
            "challenge": message,
            "signature": signature
        };
        const isSuccess = await sendResponse(voterData, '/voting/verifyVoter');
        if (isSuccess) {
            setStatus("Success!");
            console.log("Voter registration successful!");
        } else {
            setStatus("Failed");
            console.log("Voter registration failed.");
        }
        saveData(voterData);
    };

    // const [result, setResult] = useState<string>("");
    // const { ref } = useZxing({
    //   onDecodeResult(result) {
    //     setResult(result.getText());
    //   },
    // });

    return(
        <div className="h-screen flex justify-center items-center"
        style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
            <h1> Input your information</h1>
            <p>{status}</p>

        <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
            <FormField
                control={form.control}
                name="id"
                render={({ field }) => (
                <FormItem>
                    <FormLabel>id</FormLabel>
                    <FormControl>
                    <Input placeholder="input your id" {...field} />
                    </FormControl>
                    <FormMessage />
                </FormItem>
                )}
            />
            <Button type="submit">Submit</Button>
            </form>
        </Form>
        <Button>
        <Link href="/voter/voting/candidate">next page</Link>
        </Button>
            {/* <video ref={ref} />
            <p>
                <span>Last result:</span>
                <span>{result}</span>
            </p> */}
        </div>
    )
}

export default VotingTop