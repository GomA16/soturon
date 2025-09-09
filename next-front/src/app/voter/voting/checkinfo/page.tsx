"use client";

import { Button } from "@/components/ui/button";
import { useRouter } from "next/navigation";
import React, { useEffect, useState } from "react";

const BACKEND_URL = "http://localhost:8000";

const CheckInfo = () => {
    const router = useRouter();
    const [ballot, setBallot] = useState<string | null>("");
    useEffect(() => {
        setBallot(sessionStorage.getItem("ballot"));
        // console.log(ballot)
    },[]);
    const handleSubmit = async() => {
        try {
            // console.log(JSON.parse(ballot));
            const response = await fetch(BACKEND_URL+"/voting/submitBallot",{
                method:"POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: ballot});

            const data = await response.json();
            console.log(data)

            if(data.status == "success") {
                router.push("/voter/voting/complete");
            }
        }catch (error) {
            console.log("ballot sumbittion error", error)
        }
    }
    return(
        <div className="h-screen flex justify-center items-center"
        style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
            <h1>this is your ballot</h1>
            <p>{ballot}</p>
            <Button onClick={handleSubmit}>submit</Button>
        </div>
    )
};

export default CheckInfo;
