import { x24 } from "@esri/calcite-ui-icons";
import SideBar from "./SideBar";

export default function FloatingDashboard() {
  return (
    <div className="m-5 flex h-[80vh] w-[30vw] flex-row gap-5 rounded-lg bg-white text-black">
      <aside className="w-[20%] rounded-lg bg-gray-200 p-3">
        <SideBar />
      </aside>

      <main className="flex-1 rounded-lg bg-white p-3">
        <section className="mb-5 flex flex-row justify-between">
          <h1 className="text-2xl font-black">Parcel Overview</h1>
          <div className="flex flex-row items-center">
            <div className="cursor-pointer hover:text-blue-600">
              <svg className="h-6 w-6" viewBox="0 0 24 24" fill="currentColor">
                <path d={x24} />
              </svg>
            </div>
          </div>
        </section>
        <section>{/* <OwnerInformation /> */}</section>
      </main>
    </div>
  );
}
