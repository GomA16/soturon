"use client";

import React, { useEffect, useState} from "react";
import { BACKEND_URL } from "@/src/config/constants";
import { Button } from "@/components/ui/button";
import electionData from "@/data/electionData.json";
import  Link  from "next/link";

const checkAuthority = () => {
    const [status, setStatus] = useState("loading...");
    let voterData;
    console.log("voterData", voterData)
    let challenge = 0;
    // いったんjsonからデータを読み出す
    const keys = electionData.officialKey;

    // チャレンジを受け取る
    const getChallenge = async () => {
        try{
            const response = await fetch(BACKEND_URL+"/registration/challenge");
            if (!response.ok) {
                console.log("errordayon")
            }
            const data = await response.json();
            challenge = data.challenge;
            console.log("challenge", challenge);
        }catch (error) {
            console.log('challenge error', error);
        }
    };
    const dataToSign = {
        "voterData": voterData,
        "challenge": challenge
    }
    // 署名の生成
    let signature: string = "";
    const signKey = keys.signKey;
    const message: string = Buffer.from(JSON.stringify(dataToSign)).toString("base64");
    const genSignature = async () => {
        const response = await fetch('http://localhost:3000/api/sign', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ "message": message, "signKey": signKey }),
        });
        // console.log("sigresponse:\n",response);
        const data = await response.json();
        signature = data.signature;
    };
    // レスポンス生成
    const sendResponse = async () => {
        const requestData = {
            "message": message,
            "signature": signature
        };
        console.log("requestData\n",requestData);
        try{
            const response = await fetch(BACKEND_URL+"/registration/verifyOfficial",{
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(requestData),
            });
            if (!response.ok) {
                throw new Error("Failed to submit data");
            }

            const data = await response.json();

            if(data.status == "success") {
                setStatus("success!!");
                console.log("success!!");
            }
        }catch (error) {
            console.log("response error", error);
        }
    };
    const handleProcess = async () => {
        await getChallenge();
        await genSignature();
        await sendResponse();
        sessionStorage.setItem("officialKeys", JSON.stringify(electionData.officialKey));
    };

    useEffect(() => {
        voterData = sessionStorage.getItem("voterData");
        handleProcess()}, []);

    return (
        <div className="h-screen flex justify-center items-center"
        style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
            <h1>Read Officials Code</h1>
            <p>{status}</p>
            <Button>
                <Link href = "/voter/registration/pin">next</Link>
            </Button>
        </div>
    )
};

export default checkAuthority;