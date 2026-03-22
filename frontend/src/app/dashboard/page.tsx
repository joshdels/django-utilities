import FloatingDashboard from "@/features/dashboard/sidebar/FloatingDashboard";
import SearchPanel from "@/features/dashboard/sidebar/SearchSection";
import DemoMap from "@/features/homepage/demo/DemoMap";
import MapNavbar from "@/features/dashboard/navbar/MapNavbar";

export default function Project() {
  return (
    <div className="flex h-screen flex-col">
      <MapNavbar />

      <div className="relative flex-1">
        <DemoMap />

        <div className="absolute top-0 left-0 z-50">
          <SearchPanel />
          <FloatingDashboard />
        </div>
      </div>
    </div>
  );
}
