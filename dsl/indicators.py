from typing import Dict, Tuple, List, Any


SUPPORTED_INDICATORS: Dict[str, Tuple[List[str], List[str]]] = {

    "SMA": (["series", "period"], ["series", "int"]),

    "RSI": (["series", "period"], ["series", "int"])

}


def canonicalize_name(name: str) -> str:
    "Convert indicator name to canonical form"

    return name.strip().upper()


def is_supported(name: str) -> bool:
    "Check if indicator name is supported by DSL"

    return canonicalize_name(name) in SUPPORTED_INDICATORS


def validate_args(name: str, args: List[Any]) -> Tuple[bool, str]:
    "Validate number of arguments for an indicator call"

    canonical = canonicalize_name(name)

    if not is_supported(name):
        return False, f"Unsupported indicator: {name!r}"
    
    expected_arg_names, _ = SUPPORTED_INDICATORS[canonical]  
    expected_count = len(expected_arg_names)
    actual_count = len(args)

    if actual_count != expected_count:
        return (
            False,
            f"{canonical} expects {expected_count} args {tuple(expected_arg_names)}, got {actual_count}",
        )
    
    return True, "ok"


def get_indicator_signature(name: str) -> Tuple[List[str], List[str]]:
    "Get the (arg_names, arg_types_hint) tuple for a given indicator"

    canonical = canonicalize_name(name)  
    
    return SUPPORTED_INDICATORS[canonical]