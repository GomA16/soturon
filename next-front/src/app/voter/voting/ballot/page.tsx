"use client";

import { useRouter } from "next/navigation";
import React, {useEffect, useState} from "react";

const BACKEND_URL = "http://localhost:8000";

const checkInfo = () => {
    return(
        <div>
            <p>this is your encrypted ballot: make sure to see this in bulletin board</p>
        </div>
    )
};

export default checkInfo;