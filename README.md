# Native ESXi SDHCI driver for Raspberry Pi 5 / BRCM5D12

Enable the Raspberry Pi 5 microSD controller as native storage in VMware ESXi-Arm.

**[English](#english) | [Русский](#русский) | [Releases](https://github.com/Soulveig/native-esxi-driver-brcm5d12-rpi5/releases)**

> **Experimental CommunitySupported driver.** Secure Boot must be disabled. Keep physical-console access and a tested bootbank rollback available before installation.

## English

### What this project does

Raspberry Pi 5 UEFI exposes the onboard microSD controller to ESXi as the ACPI device `BRCM5D12`. The stock ESXi-Arm `vmksdhci` package does not bind to that identifier, so the card is not available as a storage device or VMFS datastore.

This package adapts VMware's existing `vmksdhci` driver family, which already contains Raspberry Pi 4-era `BCM2847` SDHCI support. It retains the original SDHCI implementation and adds the Raspberry Pi 5 `BRCM5D12` ACPI identifier and device mapping.

This is an adaptation of the existing SDHCI implementation rather than a new driver written from scratch.

### Compatibility

| Component | Validated configuration |
| --- | --- |
| Board | Raspberry Pi 5 |
| Firmware | UEFI exposing ACPI device `BRCM5D12` |
| Hypervisor | ESXi-Arm 8.0U3c build 24449057 |
| Package | Unsigned `CommunitySupported` VIB |
| Secure Boot | Disabled |
| Storage adapter | `vmhba64` |
| Tested card | 64 GB SDHC |
| Datastore | GPT + VMFS6 |

Other ESXi builds, firmware versions, boards and SD cards have not yet been validated.

### Installation

Download the standalone VIB or offline bundle from [Releases](https://github.com/Soulveig/native-esxi-driver-brcm5d12-rpi5/releases). Copy it to an ESXi datastore and enter maintenance mode.

```sh
esxcli software vib install \
  -v /vmfs/volumes/datastore1/vmksdhci-0.1.0-1-community.vib
```

Replace `datastore1` with the actual datastore name. Reboot is required because live installation and removal are intentionally disabled. Do not reboot until a known-good bootbank rollback and console access are available.

After reboot:

```sh
esxcli storage core adapter list
esxcli storage core device list
esxcli storage filesystem list
```

Expected result: the SD controller creates a storage adapter such as `vmhba64`, and an inserted card appears under `/vmfs/devices/disks/`.

### Host validation

The v0.1.0 payload was validated on a Raspberry Pi 5 host:

- `BRCM5D12` attached to `vmksdhci` and created `vmhba64`;
- a 64 GB SDHC card was detected as a native direct-access device;
- the card was partitioned with GPT and formatted as VMFS6;
- the `sd-datastore` volume mounted successfully;
- four synchronous 1 MiB write/read cycles completed with identical SHA-256 `30e14955ebf1352266dc2ff8067e68104607e750abb9d3b36582b8af909fcb58`;
- no new data I/O timeout or reset errors were observed during those cycles.

Unsupported SCSI Inquiry/VPD pages may be logged because an SD card does not expose the complete identity and management feature set of a conventional SCSI disk. These messages did not prevent VMFS operation in the validated configuration.

### Known limitations

- long-duration read/write stress has not yet been completed;
- datastore persistence after an additional cold boot is not part of the v0.1.0 validation claim;
- VPD identifiers, MMC lifetime data and some SCSI management commands are unsupported;
- the package targets only the ESXi-Arm build shown above;
- the VIB is unsigned and intended for controlled experimental use.

### Rollback

Do not rely on `esxcli software vib remove -n vmksdhci` as the only rollback: that can remove the SDHCI package without restoring VMware's original module. Preserve the original `vmksdhci.v00` or a known-good alternate bootbank before installation, and restore the original package from console/bootbank recovery if the host does not boot correctly.

## Русский

### Что делает этот проект

UEFI Raspberry Pi 5 передаёт встроенный контроллер microSD в ESXi как ACPI-устройство `BRCM5D12`. Штатный пакет ESXi-Arm `vmksdhci` не привязывается к этому идентификатору, поэтому карта не появляется как storage-устройство и не может использоваться для VMFS datastore.

Этот пакет адаптирует существующее семейство драйверов VMware `vmksdhci`, в котором уже была поддержка SDHCI Raspberry Pi 4 (`BCM2847`). Исходная реализация SDHCI сохранена; добавлены ACPI-идентификатор Raspberry Pi 5 `BRCM5D12` и соответствующее сопоставление устройства.

Это адаптация существующей реализации SDHCI, а не новый драйвер, написанный с нуля.

### Совместимость

| Компонент | Проверенная конфигурация |
| --- | --- |
| Плата | Raspberry Pi 5 |
| Прошивка | UEFI передаёт ACPI-устройство `BRCM5D12` |
| Гипервизор | ESXi-Arm 8.0U3c build 24449057 |
| Пакет | Неподписанный VIB `CommunitySupported` |
| Secure Boot | Отключён |
| Storage adapter | `vmhba64` |
| Проверенная карта | SDHC 64 ГБ |
| Datastore | GPT + VMFS6 |

Другие сборки ESXi, версии UEFI, платы и SD-карты пока не проверялись.

### Установка

Скачайте отдельный VIB или offline bundle со страницы [Releases](https://github.com/Soulveig/native-esxi-driver-brcm5d12-rpi5/releases), скопируйте файл на datastore ESXi и переведите хост в maintenance mode.

```sh
esxcli software vib install \
  -v /vmfs/volumes/datastore1/vmksdhci-0.1.0-1-community.vib
```

Замените `datastore1` фактическим именем datastore. Требуется перезагрузка: live install и live remove намеренно запрещены. Не перезагружайте хост, пока не подготовлены проверенный rollback bootbank и доступ к физической консоли.

После загрузки:

```sh
esxcli storage core adapter list
esxcli storage core device list
esxcli storage filesystem list
```

Ожидаемый результат: SD-контроллер создаёт адаптер наподобие `vmhba64`, а установленная карта появляется в `/vmfs/devices/disks/`.

### Проверка на хосте

Payload v0.1.0 проверен на Raspberry Pi 5:

- `BRCM5D12` подключился к `vmksdhci` и создал `vmhba64`;
- SDHC-карта 64 ГБ определилась как нативное direct-access устройство;
- карта размечена GPT и отформатирована в VMFS6;
- том `sd-datastore` успешно смонтирован;
- четыре синхронных цикла записи/чтения по 1 МБ завершились с одинаковым SHA-256 `30e14955ebf1352266dc2ff8067e68104607e750abb9d3b36582b8af909fcb58`;
- во время этих циклов не появилось новых ошибок data I/O, timeout или reset.

В журнале возможны сообщения о неподдерживаемых страницах SCSI Inquiry/VPD: SD-карта не предоставляет полный набор идентификаторов и управляющих функций обычного SCSI-диска. В проверенной конфигурации эти сообщения не мешали работе VMFS.

### Известные ограничения

- длительный нагрузочный тест чтения и записи пока не завершён;
- повторное автоматическое монтирование datastore после дополнительного cold boot не входит в подтверждённый статус v0.1.0;
- VPD-идентификаторы, MMC lifetime data и часть управляющих команд SCSI не поддерживаются;
- пакет предназначен только для указанной сборки ESXi-Arm;
- VIB не подписан и предназначен для контролируемых экспериментов.

### Откат

Не используйте `esxcli software vib remove -n vmksdhci` как единственный способ отката: команда может удалить пакет SDHCI, не восстановив оригинальный модуль VMware. До установки сохраните исходный `vmksdhci.v00` или проверенный альтернативный bootbank. Если хост не загрузится штатно, восстановите оригинальный пакет через консоль или bootbank recovery.

## Files / Файлы

- `vmksdhci-0.1.0-1-community.vib` — standalone VIB;
- `vmksdhci-0.1.0-1-offline-bundle.zip` — offline bundle;
- `SHA256SUMS` — контрольные суммы SHA-256.
