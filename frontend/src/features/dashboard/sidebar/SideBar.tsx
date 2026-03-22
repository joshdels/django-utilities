import {
  basemap24,
  clearSelection24,
  legendLeft24,
  waterDrop24,
} from "@esri/calcite-ui-icons";

export interface NavigationProps {
  label: string;
  icon: string;
}

const navigations: NavigationProps[] = [
  { label: "Overview", icon: clearSelection24 },
  { label: "Legends", icon: legendLeft24 },
  { label: "Basemap ", icon: basemap24 },
  { label: "Water", icon: waterDrop24 },
];

export default function SideBar() {
  return (
    <div className="flex flex-col gap-4 p-2">
      {navigations.map((nav) => (
        <div
          key={nav.label}
          className="flex flex-col items-center gap-1 p-3 cursor-pointer hover:bg-blue-500 rounded-md"
        >
          <svg className="w-6 h-6" viewBox="0 0 24 24" fill="currentColor">
            <path d={nav.icon} />
          </svg>

          <span className="font-medium text-black text-sm ">{nav.label}</span>
        </div>
      ))}
    </div>
  );
}
