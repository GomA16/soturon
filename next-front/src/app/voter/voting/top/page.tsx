"use client";

import { Button } from "@/components/ui/button";
import { useRouter } from "next/navigation";

import React, {useState} from "react";

const BACKEND_URL = "http://localhost:8000";

const VotingTop = () => {
    const router = useRouter();

    const [formData, setFormData] = useState({
        "name":"",
        "Age":"",
        "Gender":"",
    });

    const[responseMessage, setResponseMessage] = useState("");

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
      };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try{
            const response = await fetch(BACKEND_URL+"/voting",{
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(formData),
            }
            );
            if (!response.ok) {
                throw new Error("Failed to submit data");
            }

            const data = await response.json();
            setResponseMessage(`Success: ${data.message}`);

            if(data.status == "success") {
                sessionStorage.setItem("votingData", JSON.stringify(formData));
                router.push("/voter/voting/pin");
            }
        }catch(error) {
            console.error("Error:", error);
            setResponseMessage("Failed to submit the form");
        }
    };

    return(
        <div>
            <h1> Input your information</h1>
            <form onSubmit={handleSubmit}>
                <div>
                <label>Username:</label>
                <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    placeholder="Enter your name"
                />
                </div>
                <div>
                <label>Age:</label>
                <input
                    type="number"
                    name="Age"
                    value={formData.Age}
                    onChange={handleChange}
                    placeholder="Enter your age"
                />
                </div>
                <div>
                <label>Gender:</label>
                <input
                    type="text"
                    name="Gender"
                    value={formData.Gender}
                    onChange={handleChange}
                    placeholder="Enter your gender"
                />
                </div>
                <Button type="submit">Submit</Button>
            </form>
            {responseMessage && <p>{responseMessage}</p>}
    </div>
    )
}

export default VotingTop