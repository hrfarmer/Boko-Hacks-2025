import { Dialog, DialogContent, DialogTrigger } from "@/components/ui/dialog";
import DocumentCard from "./apps/DocumentUpload";
import NewsCard from "./apps/News";
import NotesCard from "./apps/Notes";

const CARDS: CardData[] = [
  {
    title: "Company News",
    description: "Stay updated with the latest business and industry news.",
    component: NewsCard,
  },
  {
    title: "Notes App",
    description:
      "A simple note-taking platform for jotting down tasks, ideas, and reminders.",
    component: NotesCard,
  },
  {
    title: "Document Upload",
    description:
      "Upload and store your PDF files for easy sharing with teammates.",
    component: DocumentCard,
  },
];

export default function Home() {
  return (
    <div className="container mx-auto p-4">
      <section className="text-center">
        <h1 className="text-4xl font-bold mb-4">Welcome to BokoHacks 2025</h1>
        <p className="text-lg mb-8">
          An Application Security Challenge Platform for Texas State
          University's 2025 BokoHacks
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {CARDS.map((card, idx) => (
            <AppCard data={card} key={idx} />
          ))}
        </div>
      </section>
    </div>
  );
}

type CardData = {
  title: string;
  description: string;
  image?: string;
  component: () => React.ReactElement;
};

function AppCard({ data }: { data: CardData }) {
  return (
    <Dialog>
      <DialogTrigger>
        <div className="app-card p-4 bg-white rounded-lg shadow-md">
          <h3 className="text-xl font-semibold mb-2">{data.title}</h3>
          <p className="text-gray-700 mb-4">{data.description}</p>
        </div>
      </DialogTrigger>
      <DialogContent className="w-200 h-230">
        <data.component />
      </DialogContent>
    </Dialog>
  );
}
