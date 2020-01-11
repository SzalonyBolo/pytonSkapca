from decimal import Decimal

sellers = {}
sellers["a"] = []
sellers["a"].append([])
sellers["a"][0].append("asdf")
sellers["a"][0].append(Decimal("0.01"))
sellers["a"].append([])
sellers["a"][1].append("zxcv")
sellers["a"][1].append(Decimal("0.10"))
sellers["a"].append([])
sellers["a"][2].append("qwert")
sellers["a"][2].append(Decimal("0.2"))

sellers["b"] = []
sellers["b"].append([])
sellers["b"][0].append("sdfg")
sellers["b"][0].append(Decimal("1.01"))
sellers["b"].append([])
sellers["b"][1].append("xcvb")
sellers["b"][1].append(Decimal("51.10"))
sellers["b"].append([])
sellers["b"][2].append("werty")
sellers["b"][2].append(Decimal("10.12"))

list(max(sellers["a"], key=lambda x:x[1]))