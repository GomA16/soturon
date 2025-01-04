import Link from "next/link";
import { Button } from "../components/button";

const VoterTop = () => {
    return(
        <div className="contaier mx-auto">
            <h1>Voter Top Page</h1>
            <Link href="/voter/registration/top">
            <Button>Sing up</Button>
            </Link>
            <Link href="/voter/voting/top">
            <Button>Vote</Button>
            </Link>
        </div>
    )
}

export default VoterTop