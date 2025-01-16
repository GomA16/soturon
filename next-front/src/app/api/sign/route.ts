
import { createSign } from 'crypto';
import { NextRequest, NextResponse } from 'next/server';

export async  function POST(req: NextRequest) {
    try{
        const body = await req.json();
        const { message, signKey } = body;

        const sign = createSign('SHA256');
        sign.update(message);
        sign.end();
        const signature = sign.sign(signKey, 'base64');

        console.log("Signature generated:", signature);

        return NextResponse.json({ "signature":signature });
    }catch (error) {
        console.error("Error in signature API:", error);
        return NextResponse.json({ error: "Failed to process request" }, { status: 500 });
    }
}