"use client";

import { useRouter } from "next/navigation";

import React, {useState} from "react";

const BACKEND_URL = "http://localhost:8000";

const VotingPin = () => {
    const router = useRouter();

    const [formData, setFormData] = useState({
        "PINcode":0,
    });

    const[responseMessage, setResponseMessage] = useState("");

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
      };

    const handleClick = async (e: React.FormEvent) => {
        e.preventDefault();
        try{

            const voterInfo = sessionStorage.getItem("votingData");
            if (!voterInfo) {
                throw new Error("No");
            }

            const parseData = JSON.parse(voterInfo);
            const storeData = { ...parseData, PINcode: Number(formData.PINcode)}
            storeData.Age = Number(storeData.Age)
            console.log(storeData)
            sessionStorage.setItem("voterInfo",JSON.stringify(storeData));
            router.push("/voter/voting/candidate");
            
        }catch(error) {
            console.error("Error:", error);
            setResponseMessage("Failed");
        }
    };

    return(
        <div>
            <h1> Input your information</h1>
            {/* <form onSubmit={handleClick}> */}
                <div>
                <label>PINcode:</label>
                <input
                    type="text"
                    name="PINcode"
                    value={formData.PINcode}
                    onChange={handleChange}
                    placeholder="Enter your PINcode"
                />
                </div>
                <button type="button" onClick={handleClick}>Next</button>
            {/* </form> */}
            {responseMessage && <p>{responseMessage}</p>}
    </div>
    )
}

export default VotingPin