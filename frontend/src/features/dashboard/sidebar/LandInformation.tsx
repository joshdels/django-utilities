"use client";

import { useState } from "react";
import { mockParcels, Parcel, buildLandInformation } from "@/mock/parcels";

export default function LandInformation() {
  const [selectedParcel, setSelectedParcel] = useState<Parcel>(mockParcels[1]);
  const landInformationData = buildLandInformation(selectedParcel);

  return (
    <div className="my-8 pr-5">
      <section className="text-lg font-black mb-5">Land Information</section>

      {landInformationData.map((item, index) => (
        <div key={index} className="flex flex-row gap-5 mb-3">
          <svg
            className="w-6 h-6 text-blue-500"
            viewBox="0 0 24 24"
            fill="currentColor"
          >
            <path d={item.icon} />
          </svg>
          <span className="">{item.label}</span>
          <span className="font-semibold">{item.value}</span>
        </div>
      ))}
    </div>
  );
}
