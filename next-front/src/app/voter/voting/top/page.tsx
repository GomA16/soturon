"use client";

import { genSignature, getChallenge, sendResponse } from "@/src/app/components/authentication";
import React, {useState} from "react";
import { useRouter } from "next/navigation";
import QRScanner from "@/src/app/components/QRScanner";


const VotingTop = () => {
    const router = useRouter();
    const [status, setStatus] = useState<string>("loading...");

    const saveData = (voterData: unknown):boolean => {
        sessionStorage.setItem("voterData", JSON.stringify({voterData}));
        return true
    };

    const [scannedData, setScannedData] = useState<string>("No result yet");

    const handleDecode = async(data: string) => {
        console.log("QR Code:", typeof(data), "\n",data);
      setScannedData(data);
      const voter = JSON.parse(data);
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
          router.push("/voter/voting/candidate");
          console.log("Voter authentication successful!");
      } else {
          setStatus("Failed");
          console.log("Voter authentication failed.");
      }
      saveData(voterData);
    };

    return(
        <div className="h-screen flex justify-center items-center"
        style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
            <p>{status}</p>
            <h1>Scan your QRコード</h1>
            {/* QRScannerコンポーネントを呼び出し */}
            <QRScanner onDecode={handleDecode} />
            {/* スキャンしたデータを表示 */}
            <p>Scanned Data: {scannedData}</p>

        </div>
    )
}

export default VotingTop