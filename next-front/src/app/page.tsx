import { Link } from "lucide-react";
import Image from "next/image";
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
