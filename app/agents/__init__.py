"""
AlvGolf Agents Package

Shared utilities for all agents.
"""


def extract_cache_usage(response, agent_name: str) -> dict:
    """
    Extract token usage + prompt caching metrics from LangChain ChatAnthropic response.

    Logs a one-line summary showing cache hit/miss for easy monitoring.

    Args:
        response: LangChain AIMessage from ChatAnthropic.invoke()
        agent_name: Agent identifier for log prefix (e.g. "AgentAnalista")

    Returns:
        dict with keys: input_tokens, output_tokens, cache_read_tokens, cache_write_tokens
    """
    usage = {}
    try:
        rm = getattr(response, 'response_metadata', None) or {}
        u = rm.get('usage', {})
        usage = {
            'input_tokens': u.get('input_tokens', 0),
            'output_tokens': u.get('output_tokens', 0),
            'cache_read_tokens': u.get('cache_read_input_tokens', 0),
            'cache_write_tokens': u.get('cache_creation_input_tokens', 0),
        }

        total_in = usage['input_tokens'] + usage['cache_read_tokens'] + usage['cache_write_tokens']
        if usage['cache_read_tokens'] > 0:
            pct = usage['cache_read_tokens'] / total_in * 100 if total_in else 0
            print(f"[{agent_name}] CACHE HIT | read: {usage['cache_read_tokens']:,} tokens ({pct:.0f}%) | input: {usage['input_tokens']:,} | output: {usage['output_tokens']:,}")
        elif usage['cache_write_tokens'] > 0:
            print(f"[{agent_name}] CACHE WRITE | written: {usage['cache_write_tokens']:,} tokens | input: {usage['input_tokens']:,} | output: {usage['output_tokens']:,}")
        elif total_in > 0:
            print(f"[{agent_name}] NO CACHE | input: {usage['input_tokens']:,} | output: {usage['output_tokens']:,}")
        else:
            print(f"[{agent_name}] Token usage not available in response metadata")

    except Exception as e:
        print(f"[{agent_name}] Could not extract cache usage: {e}")

    return usage
