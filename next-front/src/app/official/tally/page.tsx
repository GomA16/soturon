// mixした後、集計作業のリクエストをバックエンドに投げて集計結果を得る
"use client"

import { Button } from "@/components/ui/button";
import { BACKEND_URL } from "@/src/config/constants";
import { useState } from "react"

const tallyBallots = () => {
    const[result, setResult] = useState("");

    const handleClick = async () => {
        try{
            const response = await fetch(BACKEND_URL+"/tally/tallyBallots");
            if (!response.ok) {
                throw new Error("era-dayo");
            }
            const data = await response.json();
            setResult(data.result);
        } catch (error) {
            console.log("tally error desu", error);
        }
    }

    return(
        <div  className="h-screen flex justify-center items-center"
        style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
            <h1>election result</h1>
            <p>{result}</p>
            <Button onClick={handleClick}>tally</Button>
        </div>
    )
}

export default tallyBallots