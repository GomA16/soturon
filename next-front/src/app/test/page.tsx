"use client"

import { BACKEND_URL } from "@/src/config/constants";
import { createSign, createVerify, generateKeyPairSync, getCurves } from "crypto";
import electionData from "@/data/electionData.json" ;
import testdata from "@/data/testdata.json";
import bigInt from "big-integer";
import { getPrimitiveRoot, getPrimeFactors, getRandomBigInt, modInverse, modPow } from "../tools/myPrimitives/numTheory";
import { ElgamalCipherText, ElgamalKeys, ElgamalPlainText, Parameters, stringToBigInt } from "../tools/myPrimitives/elgamal";
import { useEffect } from "react";

const TestElg = () => {
    let vars = electionData.election_vars
    const params = new Parameters();
    params.setParams(vars.parameters);
    const keys = new ElgamalKeys();
    keys.setKeys(vars.tallyKeys);

    const data = testdata;
    let cipheredData: String[][] = []; 
    for (const item of data) {
        const plain = new ElgamalPlainText(stringToBigInt(JSON.stringify(item)));
        console.log(plain.ptxt);
        const c = new ElgamalCipherText();
        c.encryption(params, keys, plain);
        cipheredData.push([c.ctxt[0].toString(), c.ctxt[1].toString()]);
    }
    // console.log(cipheredData)

    const sendBallots = async() => {
        try{
            const requestData = {ciphers: cipheredData};
            // console.log("Request Data:", JSON.stringify(requestData, null, 2));
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
    const { privateKey, publicKey } = generateKeyPairSync('ec', {
        namedCurve: 'prime256v1',
    });
    // const signKey = electionData.keys.sigPrivatekey;
    // const verifyKey = electionData.keys.sigPublicKey;
    const signKey = privateKey.export({ type: 'pkcs8', format: 'pem' });
    const verifyKey = publicKey.export({ type: 'spki', format: 'pem' });
    console.log('Private Key:', signKey);
    console.log('Public Key:', verifyKey);
    const jsonData = JSON.stringify(electionData.validBallots.ballot1);
    const message = Buffer.from(jsonData).toString("base64");
    const sign = createSign('SHA256');
    sign.write(message);
    sign.end();
    const signature = sign.sign(signKey, 'base64');
    const rawSignature = Buffer.from(signature, "base64");
    console.log("singkey: ", signKey);
    console.log("verifkey:", verifyKey)
    console.log("Signature length:", rawSignature.length);
 
    const sendSignature = async () => {
        try{
            const requestData ={
                message: message,
                private_key_pem: signKey,
                public_key_pem: verifyKey,
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
            {/* <li>private_key: {signKey.export({ type: 'pkcs8', format: 'pem' })}</li>
            <li>public_key: {verifyKey.export({ type: 'spki', format: 'pem' })}</li> */}
            <li>sk: {signKey}</li>
            <li>pk: {verifyKey}</li>
            <li>signature: {signature}</li>
          </ul>
        </div>
    );
}

const TestMix = () => {
    const mix = async () => {
        await fetch(BACKEND_URL + "/mix/mixBallots"); 
    };

    useEffect(() => {
        mix();
    },[]);
    return(
        <div>test page</div>
    )
}

const TestTally = () => {
    const tally = async () => {
        await fetch(BACKEND_URL+ "/tally/tallyBallots");
    };
    useEffect(()=>{
        tally();
    },[]);
    return(
        <div>test tally</div>
    )
}

export default TestTally