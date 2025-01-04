"use client";

import { useRouter } from "next/navigation";
import React, { useEffect, useState } from "react";

const BACKEND_URL = "http://localhost:8000";

const CheckInfo = () => {
    const router = useRouter();
    const [ballotInfo, setBallotInfo] = useState<{
        name: string;
        Age: number;
        Gender: string;
        PINcode: number;
        selectedCandidate: {
            id: number;
            name: string;
            party: string;
            district: string;
        } | null;
    } | null>(null);

    useEffect(() => {
        const votinginfo = sessionStorage.getItem("votingInfo");
        if (!votinginfo) {
            throw new Error("No votingInfo");
        }
        const parseData = JSON.parse(votinginfo);
        setBallotInfo(parseData);
    }, []);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            if (!ballotInfo) return;

            const ballotData = {
                name: ballotInfo.name,
                PINcode: ballotInfo.PINcode,
                selectedCandidate: ballotInfo.selectedCandidate,
            };

            const response = await fetch(`${BACKEND_URL}/voting/addballot`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(ballotData),
            });

            if (!response.ok) {
                throw new Error("Failed to submit data");
            }

            const data = await response.json();

            if (data.status == "success") {
                router.push("/voter/voting/checkballot");
            }
        } catch (error) {
            console.error("Error:", error);
        }
    };

    if (!ballotInfo) {
        return <p>Loading...</p>;
    }

    return (
        <div>
            <h1>Check your ballot info</h1>
            <h2>PINcode: {ballotInfo.PINcode}</h2>
            <h2>Selected Candidate:</h2>
            {ballotInfo.selectedCandidate ? (
                <>
                    <h3>{ballotInfo.selectedCandidate.name}</h3>
                    <h3>{ballotInfo.selectedCandidate.party}</h3>
                </>
            ) : (
                <p>No candidate selected</p>
            )}
            <button type="button" onClick={handleSubmit}>Confirm</button>
        </div>
    );
};

export default CheckInfo;
