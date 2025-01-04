

import { BACKEND_URL } from "@/src/config/constants";
import { createSign, createVerify, generateKeyPairSync, getCurves } from "crypto";
import electionData from "@/data/electionData.json" ;
import bigInt from "big-integer";
import { getPrimitiveRoot, getPrimeFactors, getRandomBigInt, modInverse, modPow } from "../tools/myPrimitives/numTheory";
import { ElgamalCipherText, ElgamalKeys, ElgamalPlainText, Parameters, stringToBigInt } from "../tools/myPrimitives/elgamal";

const TestElg = () => {
    let vars = electionData.election_vars
    const params = new Parameters();
    params.setParams(vars.parameters);
    const keys = new ElgamalKeys();
    keys.setKeys(vars.keys);

    const data = electionData.testdata;
    let cipheredData: String[][] = []; 
    for (const item of data) {
        const plain = new ElgamalPlainText(stringToBigInt(JSON.stringify(item)));
        const c = new ElgamalCipherText();
        c.encryption(params, keys, plain);
        cipheredData.push([c.ctxt[0].toString(), c.ctxt[1].toString()]);
    }
    console.log(cipheredData)

    const sendBallots = async() => {
        try{
            const requestData = {ciphers: cipheredData};
            console.log("Request Data:", JSON.stringify(requestData, null, 2));
            const response = await fetch(BACKEND_URL+"/test/elg", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(requestData),
            });

            if (!response.ok) {
                throw new Error("era-dayo");
            }

            console.log(response);
        }catch (error) {
            console.log("error", error);
        }
    }

    sendBallots();
}

const TestSignature = () => {
    
    console.log(getCurves())
    // const { privateKey, publicKey } = generateKeyPairSync('ec', {
    //     namedCurve: 'prime256v1',
    // });
    const privateKey = electionData.keys.sigPrivatekey;
    const publicKey = electionData.keys.sigPublicKey;
    const jsonData = JSON.stringify(electionData.validBallots.ballot1);
    const message = Buffer.from(jsonData).toString("base64");
    const sign = createSign('SHA256');
    sign.write(message);
    sign.end();
    const signature = sign.sign(privateKey, 'base64');
    const rawSignature = Buffer.from(signature, "base64");
    console.log("Signature length:", rawSignature.length);
 
    const sendSignature = async () => {
        try{
            const requestData ={
                message: message,
                private_key_pem: privateKey,
                public_key_pem: publicKey,
                enc_signature: signature
            };
            console.log("requestdata", requestData);
            const response = await fetch(BACKEND_URL+"/test/sign",{
                method: "POST",
                headers:{
                    "Content-Type": "application/json"
                } ,
                body: JSON.stringify(requestData),
            });

            if(!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const responseData = await response.json();
            if(responseData.status == "success") {
                console.log("valid", responseData);
            }else{
                console.log("test fail")
            }
        }catch (error) {
            console.log("test_submission_error" , error);
        }
    };

    sendSignature();

    return(
        <div>
          <ul>
            {/* <li>private_key: {privateKey.export({ type: 'pkcs8', format: 'pem' })}</li>
            <li>public_key: {publicKey.export({ type: 'spki', format: 'pem' })}</li> */}
            <li>signature: {signature}</li>
          </ul>
        </div>
    );
}

export default TestElg