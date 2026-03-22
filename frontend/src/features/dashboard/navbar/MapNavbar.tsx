import {
  fileReport24,
  signOut24,
  group24,
  utilityNetworkLayer24,
  projectTemplate24,
} from "@esri/calcite-ui-icons";
import Navigation from "./Navigation";

export default function MapNavbar() {
  return (
    <nav className="flex h-[8vh] items-center justify-between bg-white px-6 py-4 text-black shadow-sm">
      <h1 className="text-xl font-bold">Utility ID</h1>

      <Navigation />

      <div className="flex cursor-pointer flex-col items-center hover:text-red-600">
        <svg className="h-6 w-6" viewBox="0 0 24 24" fill="currentColor">
          <path d={signOut24} />
        </svg>
        <span className="mt-1 text-sm">Logout</span>
      </div>
    </nav>
  );
}
