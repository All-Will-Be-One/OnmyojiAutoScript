"""Read-only host/device diagnostics. No game tasks, taps, or screen changes."""
import contextlib
import json
import os
import subprocess
import sys


def main():
    name = sys.argv[1] if len(sys.argv) > 1 else os.environ.get('OAS_CONFIG', 'oas1')
    with contextlib.redirect_stdout(sys.stderr):
        import cv2
        import numpy as np
        from module.config.config import Config
        from module.device.device import Device
        from module.ocr.ppocr import TextSystem

        config = Config(name)
        device = Device(config)
        image = device.screenshot_adb()
        packages = subprocess.check_output(
            [device.adb_binary, '-s', device.serial, 'shell', 'pm', 'list', 'packages', 'onmyoji'],
            text=True, timeout=15,
        ).splitlines()
        sample = np.full((80, 320, 3), 255, np.uint8)
        cv2.putText(sample, '12345', (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 2)
        result, score = TextSystem().ocr_single_line(sample)
        report = dict(config=name, serial=device.serial, screenshot_shape=list(image.shape),
                      ocr_text=result.strip(), ocr_score=float(score),
                      game_packages=packages, game_installed=bool(packages),
                      landscape_1280x720=image.shape[:2] == (720, 1280))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if result.strip() == '12345' else 1


if __name__ == '__main__':
    raise SystemExit(main())
