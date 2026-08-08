# Native ESXi SDHCI driver for Raspberry Pi 5 / BRCM5D12

Native VMware ESXi-Arm driver package for the Raspberry Pi 5 SD controller exposed as ACPI device `BRCM5D12`. It is an adaptation of VMware's existing `vmksdhci` driver family, which already contains the Raspberry Pi 4-era `BCM2847` SDHCI support; this release extends that driver for the Raspberry Pi 5/RP1 `BRCM5D12` device.

**[English](#english) | [Русский](#русский) | [Releases](https://github.com/Soulveig/native-esxi-driver-brcm5d12-rpi5/releases)**

## English

Target: ESXi-Arm 8.0U3c build 24449057. The VIB is unsigned and uses `CommunitySupported` acceptance; Secure Boot must be disabled. Install from maintenance mode and keep a rollback path and console access available.

The change is deliberately narrow: the original SDHCI implementation is retained, while the BRCM5D12 ACPI identifier and matching map entry are added. This repository does not modify the separate RP1 network driver (`rp1sys.v00`).

```sh
esxcli software vib install -v vmksdhci-0.1.0-1-community.vib
esxcli storage core adapter rescan -A vmhba64
esxcli storage filesystem list
```

Rollback:

```sh
esxcli software vib remove -n vmksdhci
```

Host validation completed: BRCM5D12 enumerated as `vmhba64`; a 64-GB SD card was partitioned GPT, formatted VMFS6, mounted as `sd-datastore`, and four synchronous 1-MiB write/read cycles produced identical SHA-256 `30e14955ebf1352266dc2ff8067e68104607e750abb9d3b36582b8af909fcb58`. No new I/O timeout/reset errors were observed. Long-duration stress and reboot persistence remain outside this release claim.

## Русский

Нативный драйвер VMware ESXi-Arm для SD-контроллера Raspberry Pi 5, который UEFI предоставляет как ACPI-устройство `BRCM5D12`. Это адаптация существующего семейства драйверов VMware `vmksdhci`, в котором уже была поддержка SDHCI Raspberry Pi 4 (`BCM2847`); в этом релизе добавлена поддержка устройства Raspberry Pi 5/RP1 `BRCM5D12`.

Цель: ESXi-Arm 8.0U3c build 24449057. VIB неподписанный, уровень `CommunitySupported`; Secure Boot должен быть отключён. Устанавливать из maintenance mode, заранее сохранить rollback и иметь доступ к консоли.

Изменения намеренно ограничены: исходная реализация SDHCI сохранена, добавлены ACPI-идентификатор BRCM5D12 и соответствующая map-запись. Отдельный сетевой драйвер RP1 (`rp1sys.v00`) в этом репозитории не изменяется и не поставляется.

```sh
esxcli software vib install -v vmksdhci-0.1.0-1-community.vib
esxcli storage core adapter rescan -A vmhba64
esxcli storage filesystem list
```

Удаление:

```sh
esxcli software vib remove -n vmksdhci
```

Проверка на хосте: BRCM5D12 определился как `vmhba64`; SD-карта 64 ГБ размечена GPT, создан VMFS6 `sd-datastore`, выполнены четыре синхронных цикла записи/чтения по 1 МБ с одинаковым SHA-256 `30e14955ebf1352266dc2ff8067e68104607e750abb9d3b36582b8af909fcb58`. Новых ошибок I/O, timeout или reset не обнаружено. Длительный stress-тест и проверка сохранения после reboot в этот статус не включены.

## Files / Файлы

- `vmksdhci-0.1.0-1-community.vib` — standalone VIB.
- `vmksdhci-0.1.0-1-offline-bundle.zip` — offline bundle.
- `SHA256SUMS` — checksums.
