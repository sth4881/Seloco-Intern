# 영상 및 복합 USN SOC, UC5000C 개요
### SELOCO UC5000C 소개
- MyUSN에는 USN System의 핵심 기능을 담당하는 UC5000C 마이크로프로세서가 내장
- UC5000C 마이크로프로세서에는 범용 MCU SU8051과 표준 영상 처리 프로세서인 JPEG encoder가 내장되어 효율적인 영상 USN 기능 지원
- MyUSN의 SG100F에서는 FPGA로 구현된 UC5000C 사용
- MyUSN의 SN100S에서는 SoC Type으로 개발된 UC5000C_R2 USN Chip 사용
- FPGA 버전 UC5000C
  - SG100F와 SN100S는 FPGA 기반의 영상 WSN SoC가 장착된 시스템
  - SPARTAN-3E 계열 160만 게이트 용량의 FGPA가 장착되어 있음
  - Intel 8051 호환의 8bit MCU인 SU8051 코어와 JPEG encoder, 압축 영상이 저장되는 영상 저장 메모리인 code buffer memory가 통합 설계되어 구현
  - FPGA는 내부의 회로 연결 정보를 저장하는 기억장소로 SRAM이 사용되기 때문에 전원이 꺼지면 저장된 설계 데이터가 지워진다.
  - 별도의 Configuration PROM을 이용해 원하는 설계 데이터를 저장해두고 전원이 꺼졌다 켜질 때 FPGA가 다시 프로그래밍되도록 하기 위하여 FGPA와 함께 전용 PROM이 필요

