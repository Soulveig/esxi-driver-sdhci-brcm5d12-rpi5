#!/usr/bin/env python3
import argparse
import datetime
import hashlib
import os
import pathlib
import shutil
import sys


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--esximage", required=True)
    parser.add_argument("--vmtar", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    sys.path.insert(0, args.esximage)
    from vmware.esximage import Vib
    from vmware.esximage import Version
    from vmware.esximage import OfflineBundle
    from vmware.esximage.Utils import EsxGzip

    os.makedirs(args.output_dir, exist_ok=True)
    payload_path = os.path.join(args.output_dir, "vmksdhci.vgz")
    vib_path = os.path.join(
        args.output_dir, "vmksdhci-0.1.0-1-community.vib")

    with open(args.vmtar, "rb") as source, open(payload_path, "wb") as raw:
        with EsxGzip.GzipFile(
            mode="wb", compresslevel=9, fileobj=raw
        ) as compressed:
            shutil.copyfileobj(source, compressed)

    vib = Vib.ArFileVib(
        name="vmksdhci",
        version=Version.VibVersion.fromstring("0.1.0-1"),
        vendor="Soulveig",
        summary="Native BRCM5D12 SDHCI driver for Raspberry Pi 5",
        description=(
            "Native VMware ESXi-Arm SDHCI driver enabling the Raspberry Pi 5 "
            "RP1 BRCM5D12 SD controller on ESXi-Arm 8.0U3c build 24449057."
        ),
        releasedate=datetime.datetime.now(datetime.timezone.utc),
        depends=[Vib.VibRelation("vmkapi_3_0_0_0")],
        swtags=[
            "RestrictStickyFiles",
            "module",
            "driver",
            "sdkversion:8.0.3-24449057",
        ],
        acceptancelevel=Vib.ArFileVib.ACCEPTANCE_COMMUNITY,
        maintenancemode=Vib.MaintenanceMode(remove=True, install=True),
        swplatforms=[("8.0", "", Vib.SoftwarePlatform.PRODUCT_EMBEDDEDESX)],
        liveinstallok=False,
        liveremoveok=False,
        cimomrestart=False,
        statelessready=True,
        overlay=False,
    )
    payload = Vib.Payload("vmksdhci.vgz", Vib.Payload.TYPE_VGZ)
    vib.AddPayload(payload, payload_path)
    vib.packedsize = os.path.getsize(payload_path)
    vib.WriteVibFile(vib_path)

    descriptor = vib.GetDescriptorText()
    descriptor_path = os.path.join(args.output_dir, "descriptor.xml")
    with open(descriptor_path, "w", encoding="utf-8") as output:
        output.write(descriptor)
        output.write("\n")

    bundle_path = os.path.join(
        args.output_dir, "vmksdhci-0.1.0-1-offline-bundle.zip")
    if os.path.exists(bundle_path):
        os.unlink(bundle_path)
    # WriteOfflineBundle's metadata scan is non-recursive in this ESXi 8.0
    # esximage implementation, so keep the single VIB at the depot root.
    vib.relativepath = "vmksdhci-0.1.0-1-community.vib"
    vib.remotelocations = [pathlib.Path(vib_path).resolve().as_uri()]
    OfflineBundle.WriteOfflineBundle(
        bundle_path,
        vendorName="Soulveig Raspberry Pi 5 Native Drivers",
        vendorCode="SOULVEIG",
        baseimages={},
        addons={},
        manifests={},
        solutions={},
        profiles=[],
        components={},
        vibs={vib.id: vib},
        versions=["8.0.3-24449057"],
        checkAcceptance=False,
        products=[Vib.SoftwarePlatform.PRODUCT_EMBEDDEDESX],
    )

    print(vib_path)
    print(bundle_path)
    print("vib_sha256=" + sha256(vib_path))
    print("bundle_sha256=" + sha256(bundle_path))


if __name__ == "__main__":
    main()
