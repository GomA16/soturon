"use client";

import { BACKEND_URL } from "@/src/config/constants";
import { useRouter } from "next/navigation";
import React, { useEffect, useState } from "react";

const backend = BACKEND_URL;

type Candidate = {
    id: number;
    name: string;
    party: string;
    district: string;
};

const CandidateSelect = () => {
    const [candidates, setCandidates] = useState<Candidate[]>([]);
    const [selectedCandidate, setSelectedCandidate] = useState<Candidate | null>(null);
    const [isLoading, setIsLoading] = useState(true); // ローディング状態を管理
    const router = useRouter();

    useEffect(() => {
        const fetchCandidates = async () => {
            try {
                const response = await fetch(`${backend}/voting/candidates`);
                if (!response.ok) {
                    throw new Error("Failed to fetch candidates");
                }
                const data: { candidates: Candidate[] } = await response.json();
                console.log(data);
                setCandidates(data.candidates || []); 
            } catch (error) {
                console.error("Error fetching candidates:", error);
                setCandidates([]); 
            } finally {
                setIsLoading(false); 
            }
        };
        fetchCandidates();
    }, []);

    const handleClick = () => {
        if (selectedCandidate) {
            const votingInfo = sessionStorage.getItem("voterInfo");
            if (!votingInfo) {
                alert("No voter information found");
                return;
            }
            const parseData = JSON.parse(votingInfo);
            const storeData = { ...parseData, selectedCandidate: selectedCandidate };
            sessionStorage.setItem("votingInfo", JSON.stringify(storeData));
            router.push("/voter/voting/checkinfo");
        } else {
            alert("Please select a candidate");
        }
    };

    return (
        <div>
            <h1>Select a Candidate</h1>
            {isLoading ? (
                <p>Loading candidates...</p> // ローディング中のUI
            ) : (
                Array.isArray(candidates) && candidates.length > 0 ? (
                    candidates.map((candidate) => (
                        <div key={candidate.id}>
                            <input
                                type="radio"
                                id={`candidate-${candidate.id}`}
                                name="candidate"
                                value={candidate.id}
                                onChange={() => setSelectedCandidate(candidate)}
                            />
                            <label htmlFor={`candidate-${candidate.id}`}>
                                {candidate.name} ({candidate.party})
                            </label>
                        </div>
                    ))
                ) : (
                    <p>No candidates available</p> // 候補者が存在しない場合のUI
                )
            )}
            <button type="button" onClick={handleClick}>Next</button>
        </div>
    );
};

export default CandidateSelect;
