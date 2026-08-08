# Native ESXi SDHCI driver for Raspberry Pi 5 / BRCM5D12

Native VMware ESXi-Arm driver package for the Raspberry Pi 5 SD controller exposed as ACPI device `BRCM5D12`.

## English

Target: ESXi-Arm 8.0U3c build 24449057. The VIB is unsigned and uses `CommunitySupported` acceptance; Secure Boot must be disabled. Install from maintenance mode and keep a rollback path and console access available.

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

Нативный драйвер VMware ESXi-Arm для SD-контроллера Raspberry Pi 5, который UEFI предоставляет как ACPI-устройство `BRCM5D12`.

Цель: ESXi-Arm 8.0U3c build 24449057. VIB неподписанный, уровень `CommunitySupported`; Secure Boot должен быть отключён. Устанавливать из maintenance mode, заранее сохранить rollback и иметь доступ к консоли.

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
