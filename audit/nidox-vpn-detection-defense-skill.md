# nidox-vpn-detection-defense-skill

Фактический аудит-скилл находится в отдельном репозитории:

- `nidox-vpn-detection-defense-skill`

Внутри `nidox-vpn-skills` этот файл служит ссылкой на внешний аудит-модуль и фиксирует обязательное правило использования.

Codex должен использовать `nidox-vpn-detection-defense-skill` перед применением любого skill из `nidox-vpn-skills`, если этот skill входит в общую VPN-структуру данного мета-репозитория.
