import { Outlet } from "react-router";

export const PAGES: { name: string; href: string }[] = [
  { name: "Home", href: "/" },
  { name: "Admin Portal", href: "/admin" },
];

export default function Navbar() {
  return (
    <div className="h-screen w-screen flex flex-col">
      <div className="h-24 bg-[#501214] w-full flex p-5 items-center justify-between text-white">
        <div>
          <p className="font-bold text-2xl">placeholder</p>
        </div>
      </div>
      <div className="h-full w-full overflow-scroll">
        <Outlet />
      </div>
      <div className="h-12 w-full bg-[#501214] text-white">footer</div>
    </div>
  );
}
