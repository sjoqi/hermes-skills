// macOS Vision-framework OCR — no pip deps, works with only CommandLineTools.
// Use when vision_analyze is unavailable or rejects an image and you need to
// extract text/numbers from a chart, table image, or screenshot.
//
// Build:  swiftc -O ocr_vision_swift.swift -o /tmp/ocr
// Run:    /tmp/ocr <image-path>
//
// Output: one line per recognized string, sorted top-to-bottom, with the
// normalized bounding-box center so tables/charts can be reconstructed:
//   y=0.856 x=0.115  Z
//   y=0.856 x=0.225  76.8
// Group lines whose y is within ~0.015 (same table row), read x left-to-right.
//
// Tips:
// - Upscale small-text images 2x first with sips (Vision OCR is much better):
//     h=$(sips -g pixelHeight img.png | awk '/pixelHeight/{print $2}')
//     w=$(sips -g pixelWidth  img.png | awk '/pixelWidth/{print $2}')
//     sips -z $((h*2)) $((w*2)) -s format png img.png --out img_2x.png
// - minimumTextHeight=0.005 catches small chart labels; raise if noise appears.
// - OCR quirks to watch: legend+value merged on one line, glyph misreads
//   ("75171.5*" for "75/71.5*", "52.58*" for "52.5*"). Always cross-check at
//   least one row against an independent number before trusting the output.

import Foundation
import Vision
import AppKit

// Usage: ocr <image-path>
let path = CommandLine.arguments.count > 1 ? CommandLine.arguments[1] : ""
guard !path.isEmpty, let img = NSImage(contentsOfFile: path),
      let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
    print("ERR load"); exit(1)
}
let request = VNRecognizeTextRequest { req, _ in
    guard let obs = req.results as? [VNRecognizedTextObservation] else { return }
    let sorted = obs.sorted { a, b in
        let ay = a.boundingBox.midY, by = b.boundingBox.midY
        if abs(ay - by) > 0.015 { return ay > by }
        return a.boundingBox.minX < b.boundingBox.minX
    }
    for o in sorted {
        if let c = o.topCandidates(1).first {
            let bb = o.boundingBox
            print(String(format: "y=%.3f x=%.3f  %@", bb.midY, bb.minX, c.string))
        }
    }
}
request.recognitionLevel = .accurate
request.usesLanguageCorrection = false
request.minimumTextHeight = 0.005
let handler = VNImageRequestHandler(cgImage: cg, options: [:])
try? handler.perform([request])
