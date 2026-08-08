// mac_wifi.swift — macOS CoreWLAN RSSI helper for live WiFi sensing.
// Based on ruvnet/RuView (archive/v1/src/sensing/mac_wifi.swift), extended to
// also report the active link's SSID/BSSID/channel (blank on Sonoma+ due to
// redaction, but channel confirms the link; rssiValue() needs no entitlement).
//
// Emits one JSON object per line at ~10 Hz:
//   {"timestamp":<f>,"rssi":<i>,"noise":<i>,"tx_rate":<f>,"ssid":"<s>","bssid":"<s>","channel":<i>}
//
// Build:  swiftc -O mac_wifi.swift -o mac_wifi
// Use:    spawn from a Rust/Python consumer; parse each JSON line.

import Foundation
import CoreWLAN

func main() {
    guard let interface = CWWiFiClient.shared().interface() else {
        fputs("{\"error\": \"No WiFi interface found\"}\n", stderr)
        exit(1)
    }

    // Unbuffered stdout so the consumer sees samples immediately.
    setbuf(stdout, nil)

    let interval: TimeInterval = 0.1

    while true {
        let timestamp = Date().timeIntervalSince1970
        let rssi = interface.rssiValue()
        let noise = interface.noiseMeasurement()
        let txRate = interface.transmitRate()
        let ssid = interface.ssid() ?? ""
        let bssid = interface.bssid() ?? ""
        let channel = interface.wlanChannel()?.channelNumber ?? 0

        let json = "{\"timestamp\": \(timestamp), \"rssi\": \(rssi), \"noise\": \(noise), \"tx_rate\": \(txRate), \"ssid\": \"\(ssid)\", \"bssid\": \"\(bssid)\", \"channel\": \(channel)}"
        print(json)

        Thread.sleep(forTimeInterval: interval)
    }
}

main()
