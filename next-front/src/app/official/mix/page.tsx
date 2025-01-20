// バックエンドに、mixの命令をgetで飛ばして、結果を得る
"use client"

import { Button } from "@/components/ui/button";
import { BACKEND_URL } from "@/src/config/constants";
import { useState } from "react"

const mixBallots = () => {
    const [result, setResult] = useState("");
    async function handleClick() {
        try{
            const response = await fetch(BACKEND_URL + "/mix/mixBallots");            
            if (!response.ok) {
                throw new Error("era-dayo");
            }
            const data = await response.json();
            setResult(data.mixResult);
        } catch (error) {
            console.log("error desuwa", error);
        }
    } 
    return(
        <div  className="h-screen flex justify-center items-center"
        style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
            <p>{result}</p>
            <Button onClick={handleClick}>mix ballot</Button>
        </div>
    );
}

export default mixBallots