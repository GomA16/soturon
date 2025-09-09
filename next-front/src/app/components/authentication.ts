import { BACKEND_URL } from "@/src/config/constants";

export const getChallenge = async (): Promise<string | null> => {
    try{
        const response = await fetch(BACKEND_URL+"/registration/challenge");
        if (!response.ok) {
            console.log("errordayon")
        }
        const data = await response.json();
        console.log("challenge", data.challenge);
        return data.challenge;
    }catch (error) {
        console.log('challenge error', error);
        return null;
    }
};

// 署名の生成

export const genSignature = async (message: string, signKey: string): Promise<string|null> => {
    try{
        const response = await fetch('http://localhost:3000/api/sign', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ "message": message, "signKey": signKey }),
        });
        // console.log("sigresponse:\n",response);
        const data = await response.json();
        return data.signature;
    } catch (error) {
        console.error("gen sing error", error);
        return null;
    }
};

// レスポンス生成
export const sendResponse = async (responseData: unknown, apiPATH: string): Promise<boolean> => {
    try{
        const response = await fetch(BACKEND_URL+apiPATH,{
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(responseData),
        });
        if (!response.ok) {
            throw new Error("Failed to submit data");
        }
        const data = await response.json();
        if (data.status == "success") {
            return true;
        }else {
            return false;
        }
    }catch (error) {
        console.log("response error", error);
        return false;
    }
};