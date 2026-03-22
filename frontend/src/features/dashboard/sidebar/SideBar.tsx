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
          className="flex cursor-pointer flex-col items-center gap-1 rounded-md p-3 hover:bg-blue-500"
        >
          <svg className="h-6 w-6" viewBox="0 0 24 24" fill="currentColor">
            <path d={nav.icon} />
          </svg>

          <span className="text-sm font-medium text-black">{nav.label}</span>
        </div>
      ))}
    </div>
  );
}
