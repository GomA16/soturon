import Link from "next/link";
import { Button } from "@/components/ui/button";

const VoterTop = () => {
    return(
        <div className="h-screen flex justify-center items-center"
        style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
            <h1>Voter Top Page</h1>
            <Button asChild variant="pink">
            <Link href="/voter/registration/top">Sing up page</Link>
            </Button>
            
            <Button asChild variant="blue">
            <Link href="/voter/voting/top">Voting page</Link>
            </Button>
            
        </div>
    )
}

export default VoterTop