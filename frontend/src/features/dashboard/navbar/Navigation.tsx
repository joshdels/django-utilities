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
          className="flex cursor-pointer flex-col items-center hover:text-blue-600"
        >
          <svg className="h-6 w-6" viewBox="0 0 24 24" fill="currentColor">
            <path d={nav.icon} />
          </svg>
          <span className="mt-1 text-sm">{nav.label}</span>
        </div>
      ))}
    </div>
  );
}
