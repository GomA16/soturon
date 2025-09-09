// 有権者の情報を読み取る
// サーバからチャレンジを受け取る
// レスポンスをサーバーに送り、サーバー側での検証が成功したら画面遷移

"use client";

import React, { useState } from "react";
// import { BACKEND_URL } from "@/src/config/constants";
import { genSignature, getChallenge, sendResponse } from "@/src/app/components/authentication";
import { useRouter } from "next/navigation";
// import { useZxing } from "react-zxing";
import QRScanner from "@/src/app/components/QRScanner";

const RegistraionTop = () => {
    const  router = useRouter();
    const [status, setStatus] = useState<string>("loading...");
    const saveData = (voterData: unknown):boolean => {
        sessionStorage.setItem("voterData", JSON.stringify({voterData}));
        return true
    };

    const [scannedData, setScannedData] = useState<string>("No result yet");

    const handleDecode = async(data: string) => {
      setScannedData(data);
      const voter = JSON.parse(data);
    
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
          "challenge": message,
          "signature": signature
      };
      const isSuccess = await sendResponse(voterData,"/registration/verifyVoter");
      if (isSuccess) {
          setStatus("Success!");
          console.log("Voter registration successful!");
          router.push("/voter/registration/authority")
      } else {
          setStatus("Failed");
          console.log("Voter registration failed.");
      }
      saveData(voterData);
      console.log("QR Code:", typeof(data), "\n",data);
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

export default RegistraionTop