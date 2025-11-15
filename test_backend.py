"""
Backend-Test-Skript
Testet alle API-Endpunkte (erweitert)
"""
import requests
import time
import sys
import math

BACKEND_URL = "http://localhost:5000"

def timed_request(method, url, **kwargs):
    """Hilfsfunktion: misst Dauer eines Requests"""
    start = time.perf_counter()
    resp = requests.request(method, url, **kwargs)
    duration = (time.perf_counter() - start) * 1000.0
    return resp, duration

def test_health():
    """Teste Health-Endpunkt"""
    print("🔍 Teste /health...")
    try:
        response, ms = timed_request("GET", f"{BACKEND_URL}/health", timeout=5)
        print(f"   Status Code: {response.status_code} ({ms:.1f} ms)")
        print(f"   Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"   ❌ Fehler: {e}")
        return False

def test_root():
    """Teste Root-Endpunkt"""
    print("\n🔍 Teste /...")
    try:
        response, ms = timed_request("GET", f"{BACKEND_URL}/", timeout=5)
        print(f"   Status Code: {response.status_code} ({ms:.1f} ms)")
        print(f"   Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"   ❌ Fehler: {e}")
        return False

def test_predict_simple():
    """Teste Predict-Endpunkt mit einfachem Schwarzbild"""
    print("\n🔍 Teste /predict (schwarzes Bild)...")
    try:
        from PIL import Image
        import io
        import base64
        img = Image.new('L', (28, 28), color=0)
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        payload = {"image": f"data:image/png;base64,{img_base64}"}
        response, ms = timed_request("POST", f"{BACKEND_URL}/predict", json=payload, timeout=10)
        print(f"   Status Code: {response.status_code} ({ms:.1f} ms)")
        if response.status_code == 200:
            result = response.json()
            probs = result.get('all_probabilities', {})
            prob_sum = sum(probs.values()) if probs else None
            print(f"   Vorhersage: {result['prediction']}")
            print(f"   Konfidenz: {result['confidence']:.2%}")
            if prob_sum is not None:
                print(f"   Summe Wahrscheinlichkeiten: {prob_sum:.4f}")
                if not (0.99 <= prob_sum <= 1.01):
                    print("   ⚠️ Summe außerhalb erwarteter Toleranz!")
            return True
        else:
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Fehler: {e}")
        return False


def test_predict_missing_image():
    print("\n🔍 Teste /predict (fehlendes Bild)...")
    try:
        response, ms = timed_request("POST", f"{BACKEND_URL}/predict", json={}, timeout=5)
        print(f"   Status Code: {response.status_code} ({ms:.1f} ms)")
        ok = response.status_code == 400
        print(f"   Erwartet 400 -> {'✅' if ok else '❌'}")
        return ok
    except Exception as e:
        print(f"   ❌ Fehler: {e}")
        return False


def test_predict_invalid_base64():
    print("\n🔍 Teste /predict (ungültiges Base64)...")
    try:
        payload = {"image": "data:image/png;base64,%%%%NOT_BASE64%%%%"}
        response, ms = timed_request("POST", f"{BACKEND_URL}/predict", json=payload, timeout=5)
        print(f"   Status Code: {response.status_code} ({ms:.1f} ms)")
        ok = response.status_code in (400, 500)
        print(f"   Erwartet Fehlerstatus -> {'✅' if ok else '❌'}")
        return ok
    except Exception as e:
        print(f"   ❌ Fehler: {e}")
        return False


def test_predict_random_noise():
    print("\n🔍 Teste /predict (Zufallsrauschen)...")
    try:
        from PIL import Image
        import numpy as np
        import io
        import base64
        noise = (np.random.rand(28, 28) * 255).astype('uint8')
        img = Image.fromarray(noise, mode='L')
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        payload = {"image": f"data:image/png;base64,{img_base64}"}
        response, ms = timed_request("POST", f"{BACKEND_URL}/predict", json=payload, timeout=10)
        print(f"   Status Code: {response.status_code} ({ms:.1f} ms)")
        if response.status_code == 200:
            result = response.json()
            print(f"   Vorhersage: {result['prediction']} (Konfidenz {result['confidence']:.2%})")
            return True
        else:
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Fehler: {e}")
        return False

def main():
    print("=" * 60)
    print("🚀 BACKEND TEST (erweitert)")
    print("=" * 60)

    # Warte kurz, falls Backend gerade startet
    print("\n⏳ Warte 1 Sekunde...")
    time.sleep(1)

    # Teste alle Endpunkte
    results = {
        "health": test_health(),
        "root": test_root(),
        "predict_black": test_predict_simple(),
        "predict_missing": test_predict_missing_image(),
        "predict_invalid_b64": test_predict_invalid_base64(),
        "predict_noise": test_predict_random_noise(),
    }

    # Zusammenfassung
    print("\n" + "=" * 60)
    print("📊 ZUSAMMENFASSUNG")
    print("=" * 60)

    for endpoint, success in results.items():
        status = "✅ OK" if success else "❌ FEHLER"
        print(f"{endpoint:20} {status}")

    all_passed = all(results.values())
    print("\n" + ("✅ ALLE TESTS BESTANDEN!" if all_passed else "❌ EINIGE TESTS FEHLGESCHLAGEN"))

    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
