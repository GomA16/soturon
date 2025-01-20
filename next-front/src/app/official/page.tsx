import { Button } from "@/components/ui/button"
import Link from "next/link"

const officialTop= () => {
    return (
        <div  className="h-screen flex justify-center items-center"
        style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
            <Button>
                <Link href = "">start voting</Link>
            </Button>
            <Button>
                <Link href = "">end voting</Link>
            </Button>
            <Button>
                <Link href = "">mix ballots</Link>
            </Button>
            <Button>
                <Link href = "">tally ballots</Link>
            </Button>
            <Button>
                <Link href = "">publish result</Link>
            </Button>
        </div>
    )
}

export default officialTop