import { Link } from "lucide-react";
import { Button } from "./components/button";

export default function Home() {
  return (
    <div>
      Vote is coming
      <Link href="/voter">
        <Button>voter</Button>
      </Link>
    </div>
  );
}
