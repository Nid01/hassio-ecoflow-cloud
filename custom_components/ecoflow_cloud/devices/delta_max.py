from homeassistant.const import Platform

from . import const, BaseDevice, EntityMigration, MigrationAction
from .. import EcoflowMQTTClient
from ..entities import BaseSensorEntity, BaseNumberEntity, BaseSwitchEntity, BaseSelectEntity
from ..number import ChargingPowerEntity, MinBatteryLevelEntity, MaxBatteryLevelEntity, \
    MaxGenStopLevelEntity, MinGenStartLevelEntity
from ..sensor import LevelSensorEntity, RemainSensorEntity, TempSensorEntity, CyclesSensorEntity, \
    InWattsSensorEntity, OutWattsSensorEntity, StatusSensorEntity, MilliVoltSensorEntity, \
    InMilliVoltSensorEntity, OutMilliVoltSensorEntity, CapacitySensorEntity, InWattsSolarSensorEntity, \
    OutWattsDcSensorEntity, VoltSensorEntity
from ..switch import BeeperEntity, EnabledEntity


class DeltaMax(BaseDevice):
    def sensors(self, client: EcoflowMQTTClient) -> list[BaseSensorEntity]:
        return [
            LevelSensorEntity(client, "bmsMaster.f32ShowSoc", const.MAIN_BATTERY_LEVEL)
                .attr("bmsMaster.designCap", const.ATTR_DESIGN_CAPACITY, 0)
                .attr("bmsMaster.fullCap", const.ATTR_FULL_CAPACITY, 0)
                .attr("bmsMaster.remainCap", const.ATTR_REMAIN_CAPACITY, 0)
                .attr("bmsMaster.cycles", const.CYCLES, 0),
            CapacitySensorEntity(client, "bmsMaster.designCap", const.MAIN_DESIGN_CAPACITY, False),
            CapacitySensorEntity(client, "bmsMaster.fullCap", const.MAIN_FULL_CAPACITY, False),
            CapacitySensorEntity(client, "bmsMaster.remainCap", const.MAIN_REMAIN_CAPACITY, False),

            LevelSensorEntity(client, "ems.f32LcdShowSoc", const.COMBINED_BATTERY_LEVEL),
            InWattsSensorEntity(client, "pd.wattsInSum", const.TOTAL_IN_POWER),
            OutWattsSensorEntity(client, "pd.wattsOutSum", const.TOTAL_OUT_POWER),

            InWattsSensorEntity(client, "inv.inputWatts", const.AC_IN_POWER),
            OutWattsSensorEntity(client, "inv.outputWatts", const.AC_OUT_POWER),

            InMilliVoltSensorEntity(client, "inv.acInVol", const.AC_IN_VOLT),
            OutMilliVoltSensorEntity(client, "inv.invOutVol", const.AC_OUT_VOLT),

            InWattsSolarSensorEntity(client, "mppt.inWatts", const.SOLAR_IN_POWER),
            OutWattsDcSensorEntity(client, "mppt.outWatts", const.DC_OUT_POWER),

            OutWattsSensorEntity(client, "pd.typec1Watts", const.TYPEC_1_OUT_POWER),
            OutWattsSensorEntity(client, "pd.typec2Watts", const.TYPEC_2_OUT_POWER),

            OutWattsSensorEntity(client, "pd.usb1Watts", const.USB_1_OUT_POWER),
            OutWattsSensorEntity(client, "pd.usb2Watts", const.USB_2_OUT_POWER),

            OutWattsSensorEntity(client, "pd.qcUsb1Watts", const.USB_QC_1_OUT_POWER),
            OutWattsSensorEntity(client, "pd.qcUsb2Watts", const.USB_QC_2_OUT_POWER),

            RemainSensorEntity(client, "ems.chgRemainTime", const.CHARGE_REMAINING_TIME),
            RemainSensorEntity(client, "ems.dsgRemainTime", const.DISCHARGE_REMAINING_TIME),

            TempSensorEntity(client, "inv.outTemp", "Inv Out Temperature"),
            CyclesSensorEntity(client, "bmsMaster.cycles", const.CYCLES),

            TempSensorEntity(client, "bmsMaster.temp", const.BATTERY_TEMP)
                .attr("bmsMaster.minCellTemp", const.ATTR_MIN_CELL_TEMP, 0)
                .attr("bmsMaster.maxCellTemp", const.ATTR_MAX_CELL_TEMP, 0),
            TempSensorEntity(client, "bmsMaster.minCellTemp", const.MIN_CELL_TEMP, False),
            TempSensorEntity(client, "bmsMaster.maxCellTemp", const.MAX_CELL_TEMP, False),

            MilliVoltSensorEntity(client, "bmsMaster.vol", const.BATTERY_VOLT, False)
                .attr("bmsMaster.minCellVol", const.ATTR_MIN_CELL_VOLT, 0)
                .attr("bmsMaster.maxCellVol", const.ATTR_MAX_CELL_VOLT, 0),
            MilliVoltSensorEntity(client, "bmsMaster.minCellVol", const.MIN_CELL_VOLT, False),
            MilliVoltSensorEntity(client, "bmsMaster.maxCellVol", const.MAX_CELL_VOLT, False),

            #Optional Slave Battery
            LevelSensorEntity(client, "bmsSlave1.f32ShowSoc", const.SLAVE_BATTERY_LEVEL, False, True)
                .attr("bmsSlave1.designCap", const.ATTR_DESIGN_CAPACITY, 0)
                .attr("bmsSlave1.fullCap", const.ATTR_FULL_CAPACITY, 0)
                .attr("bmsSlave1.remainCap", const.ATTR_REMAIN_CAPACITY, 0)
                .attr("bmsSlave1.cycles", const.CYCLES, 0),
            
            TempSensorEntity(client, "bmsSlave1.temp", const.SLAVE_BATTERY_TEMP, False, True),
            TempSensorEntity(client, "bmsSlave1.minCellTemp", const.SLAVE_MIN_CELL_TEMP, False),
            TempSensorEntity(client, "bmsSlave1.maxCellTemp", const.SLAVE_MAX_CELL_TEMP, False),
			
            VoltSensorEntity(client, "bmsSlave1.vol", const.SLAVE_BATTERY_VOLT, False),
            VoltSensorEntity(client, "bmsSlave1.minCellVol", const.SLAVE_MIN_CELL_VOLT, False),
            VoltSensorEntity(client, "bmsSlave1.maxCellVol", const.SLAVE_MAX_CELL_VOLT, False),
			
            CapacitySensorEntity(client, "bmsSlave1.fullCap", "Slave " + const.ATTR_FULL_CAPACITY),
            CapacitySensorEntity(client, "bmsSlave1.remainCap", "Slave " + const.ATTR_REMAIN_CAPACITY),
			
            CyclesSensorEntity(client, "bmsSlave1.cycles", const.SLAVE_CYCLES),
            InWattsSensorEntity(client, "bmsSlave1.inputWatts", const.SLAVE_IN_POWER),
            OutWattsSensorEntity(client, "bmsSlave1.outputWatts", const.SLAVE_OUT_POWER),
            
            RemainSensorEntity(client, "bmsSlave1.remainTime", "Slave Battery Dis-/" + const.CHARGE_REMAINING_TIME),
            StatusSensorEntity(client),
        ]

    def numbers(self, client: EcoflowMQTTClient) -> list[BaseNumberEntity]:
        return [
            MaxBatteryLevelEntity(client, "ems.maxChargeSoc", const.MAX_CHARGE_LEVEL, 50, 100,
                                  lambda value: {"moduleType": 2, "operateType": "TCP",
                                                 "params": {"id": 49, "maxChgSoc": value}}),

            MinBatteryLevelEntity(client, "ems.minDsgSoc", const.MIN_DISCHARGE_LEVEL, 0, 30,
                                  lambda value: {"moduleType": 2, "operateType": "TCP",
                                                 "params": {"id": 51, "minDsgSoc": value}}),

            MinGenStartLevelEntity(client, "ems.minOpenOilEbSoc", const.GEN_AUTO_START_LEVEL, 0, 30,
                                   lambda value: {"moduleType": 2, "operateType": "TCP",
                                                  "params": {"id": 52, "openOilSoc": value}}),

            MaxGenStopLevelEntity(client, "ems.maxCloseOilEbSoc", const.GEN_AUTO_STOP_LEVEL, 50, 100,
                                  lambda value: {"moduleType": 2, "operateType": "TCP",
                                                 "params": {"id": 53, "closeOilSoc": value}}),

            ChargingPowerEntity(client, "inv.cfgFastChgWatt", const.AC_CHARGING_POWER, 200, 2000,
                                lambda value: {"moduleType": 0, "operateType": "TCP",
                                               "params": {"slowChgPower": value, "id": 69}}),

        ]

    def switches(self, client: EcoflowMQTTClient) -> list[BaseSwitchEntity]:
        return [
            BeeperEntity(client, "pd.beepState", const.BEEPER,
                         lambda value: {"moduleType": 5, "operateType": "TCP", "params": {"id": 38, "enabled": value}}),

            EnabledEntity(client, "pd.dcOutState", const.USB_ENABLED,
                          lambda value: {"moduleType": 0, "operateType": "TCP", "params": {"enabled": value, "id": 34  }}),

            EnabledEntity(client, "pd.acAutoOnCfg", const.AC_ALWAYS_ENABLED,
                          lambda value: {"moduleType": 1, "operateType": "acAutoOn", "params": {"cfg": value}}),

            EnabledEntity(client, "pd.pvChgPrioSet", const.PV_PRIO,
                          lambda value: {"moduleType": 1, "operateType": "pvChangePrio", "params": {"pvChangeSet": value}}),

            EnabledEntity(client, "inv.cfgAcEnabled", const.AC_ENABLED,
                          lambda value: {"moduleType": 0, "operateType": "TCP", "params": {"enabled": value, "id": 66  }}),

            EnabledEntity(client, "inv.cfgAcXboost", const.XBOOST_ENABLED,
                          lambda value: {"moduleType": 5, "operateType": "TCP", "params": {"id": 66, "xboost": value}}),

            EnabledEntity(client, "mppt.carState", const.DC_ENABLED,
                          lambda value: {"moduleType": 0, "operateType": "TCP", "params": {"enabled": value, "id": 81  }}),

        ]

    def selects(self, client: EcoflowMQTTClient) -> list[BaseSelectEntity]:
        return [
            #DictSelectEntity(client, "mppt.cfgDcChgCurrent", const.DC_CHARGE_CURRENT, const.DC_CHARGE_CURRENT_OPTIONS,
            #                 lambda value: {"moduleType": 5, "operateType": "dcChgCfg",
            #                                "params": {"dcChgCfg": value}}),

            #TimeoutDictSelectEntity(client, "pd.lcdOffSec", const.SCREEN_TIMEOUT, const.SCREEN_TIMEOUT_OPTIONS,
            #                        lambda value: {"moduleType": 1, "operateType": "lcdCfg",
            #                                       "params": {"brighLevel": 255, "delayOff": value}}),

            #TimeoutDictSelectEntity(client, "inv.cfgStandbyMin", const.UNIT_TIMEOUT, const.UNIT_TIMEOUT_OPTIONS,
            #                        lambda value: {"moduleType": 1, "operateType": "standbyTime",
            #                                       "params": {"standbyMin": value}}),

            #TimeoutDictSelectEntity(client, "mppt.acStandbyMins", const.AC_TIMEOUT, const.AC_TIMEOUT_OPTIONS,
            #                        lambda value: {"moduleType": 5, "operateType": "standbyTime",
            #                                       "params": {"standbyMins": value}}),

            #TimeoutDictSelectEntity(client, "mppt.carStandbyMin", const.DC_TIMEOUT, const.DC_TIMEOUT_OPTIONS,
            #                        lambda value: {"moduleType": 5, "operateType": "carStandby",
            #                                       "params": {"standbyMins": value}})

        ]

    def migrate(self, version) -> list[EntityMigration]:
        if version == 2:
            return [
                EntityMigration("pd.soc", Platform.SENSOR, MigrationAction.REMOVE),
            ]
        return []
