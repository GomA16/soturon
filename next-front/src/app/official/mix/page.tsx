// バックエンドに、mixの命令をgetで飛ばして、結果を得る
"use client"

import { Button } from "@/components/ui/button";
import { BACKEND_URL } from "@/src/config/constants";

const MixBallots = () => {
        const handleClick = async () => {
            await fetch(BACKEND_URL + "/mix/mixBallots"); 
        };

        return(
            <div  className="h-screen flex justify-center items-center"
            style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
                <h1>test page</h1>
                <Button onClick={handleClick}>mix</Button>
            </div>
        )
    
}

export default MixBallots