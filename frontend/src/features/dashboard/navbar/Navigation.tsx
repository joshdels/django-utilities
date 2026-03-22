import {
  fileReport24,
  group24,
  projectTemplate24,
  utilityNetwork24,
} from "@esri/calcite-ui-icons";

export interface NavbarNavigation {
  label: string;
  icon: string;
}

const navigations: NavbarNavigation[] = [
  { label: "Project", icon: projectTemplate24 },
  { label: "Utility Map", icon: utilityNetwork24 },
  { label: "Teams", icon: group24 },
  { label: "Report", icon: fileReport24 },
];

export default function Navigation() {
  return (
    <div className="flex items-center gap-10">
      {navigations.map((nav, index) => (
        <div
          key={index}
          className="flex flex-col items-center cursor-pointer hover:text-blue-600"
        >
          <svg className="w-6 h-6" viewBox="0 0 24 24" fill="currentColor">
            <path d={nav.icon} />
          </svg>
          <span className="text-sm mt-1">{nav.label}</span>
        </div>
      ))}
    </div>
  );
}
