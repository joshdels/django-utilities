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
    <nav className="flex items-center justify-between px-6 py-4 bg-white text-black shadow-sm h-[8vh]">
      <h1 className="text-xl font-bold">Utility ID</h1>

      <Navigation />

      <div className="flex flex-col items-center cursor-pointer hover:text-red-600">
        <svg className="w-6 h-6" viewBox="0 0 24 24" fill="currentColor">
          <path d={signOut24} />
        </svg>
        <span className="text-sm mt-1">Logout</span>
      </div>
    </nav>
  );
}
