"""
Test script for FreeLLM client.

Run this script to verify that the client is working correctly.
"""

import asyncio
import logging
from client import FreeLLMClient
from config import FreeLLMConfig
from utils import setup_logging, format_response_for_display
from exceptions import FreeLLMError


async def test_basic_chat():
    """Test basic chat functionality."""
    print("\n" + "="*60)
    print("TEST 1: Basic Chat")
    print("="*60)

    try:
        async with FreeLLMClient(timeout=30.0) as client:
            response = await client.chat("Hello! Can you hear me?")
            print(f"\n✅ Success!")
            print(f"Response: {response.response}")
            return True
    except FreeLLMError as e:
        print(f"\n❌ Failed: {e}")
        return False


async def test_chat_with_parameters():
    """Test chat with custom parameters."""
    print("\n" + "="*60)
    print("TEST 2: Chat with Parameters")
    print("="*60)

    try:
        async with FreeLLMClient() as client:
            response = await client.chat(
                message="Write a haiku about coding",
                temperature=0.8,
                max_tokens=100,
            )
            print(f"\n✅ Success!")
            print(f"Response: {response.response}")

            if response.model:
                print(f"Model: {response.model}")
            if response.usage:
                print(f"Usage: {response.usage}")

            return True
    except FreeLLMError as e:
        print(f"\n❌ Failed: {e}")
        return False


async def test_conversation_context():
    """Test conversation with context."""
    print("\n" + "="*60)
    print("TEST 3: Conversation with Context")
    print("="*60)

    try:
        async with FreeLLMClient() as client:
            # First message
            print("\nUser: My favorite color is blue")
            response1 = await client.chat_with_context("My favorite color is blue")
            print(f"AI: {response1.response}")

            # Second message (should remember context)
            print("\nUser: What's my favorite color?")
            response2 = await client.chat_with_context("What's my favorite color?")
            print(f"AI: {response2.response}")

            # Check history
            history = client.get_history()
            print(f"\n✅ Success! Conversation has {len(history.messages)} messages")
            return True

    except FreeLLMError as e:
        print(f"\n❌ Failed: {e}")
        return False


async def test_configuration():
    """Test configuration loading."""
    print("\n" + "="*60)
    print("TEST 4: Configuration")
    print("="*60)

    try:
        config = FreeLLMConfig.from_env()
        print(f"\n✅ Configuration loaded successfully!")
        print(f"  Base URL: {config.base_url}")
        print(f"  Timeout: {config.timeout}s")
        print(f"  Max Retries: {config.max_retries}")
        print(f"  Default Temperature: {config.default_temperature}")
        return True
    except Exception as e:
        print(f"\n❌ Failed: {e}")
        return False


async def test_error_handling():
    """Test error handling."""
    print("\n" + "="*60)
    print("TEST 5: Error Handling")
    print("="*60)

    # Test with invalid base URL
    client = FreeLLMClient(base_url="https://invalid-url-that-does-not-exist.com")

    try:
        await client.chat("This should fail")
        print(f"\n❌ Should have raised an exception!")
        return False
    except FreeLLMError as e:
        print(f"\n✅ Successfully caught error: {type(e).__name__}")
        print(f"  Message: {str(e)[:100]}")
        return True
    finally:
        await client.close()


async def run_all_tests():
    """Run all tests."""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*15 + "FreeLLM Client Test Suite" + " "*18 + "║")
    print("╚" + "="*58 + "╝")

    tests = [
        test_configuration,
        test_error_handling,
        test_basic_chat,
        test_chat_with_parameters,
        test_conversation_context,
    ]

    results = []
    for test in tests:
        try:
            result = await test()
            results.append((test.__name__, result))
        except Exception as e:
            print(f"\n❌ Test {test.__name__} crashed: {e}")
            results.append((test.__name__, False))

    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")

    print("\n" + "-"*60)
    print(f"Results: {passed}/{total} tests passed")
    print("="*60 + "\n")

    return passed == total


if __name__ == "__main__":
    # Setup logging
    setup_logging(level=logging.WARNING)

    # Run tests
    success = asyncio.run(run_all_tests())

    exit(0 if success else 1)
