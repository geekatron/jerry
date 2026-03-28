# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""RED phase tests for ``jerry proxy`` CLI namespace.

All tests in this module MUST FAIL until TASK-023-076 (parser) and
TASK-023-077 (handler) implement the proxy namespace.  These tests
define the contract that the GREEN phase must satisfy.

References:
    - TASK-023-075: BDD tests for jerry proxy CLI namespace
    - STORY-023-022: Jerry CLI Proxy Namespace Integration
    - H-20: BDD Red phase -- tests written before implementation
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from src.interface.cli.parser import create_parser

# ---------------------------------------------------------------------------
# Parser tests: ``jerry proxy`` namespace registration
# ---------------------------------------------------------------------------


class TestProxyCredentialsSetParser:
    """``jerry proxy credentials set <provider>`` parses correctly."""

    def test_parse_when_valid_provider_then_namespace_is_proxy(self) -> None:
        parser = create_parser()
        args = parser.parse_args(["proxy", "credentials", "set", "digitalocean"])
        assert args.namespace == "proxy"

    def test_parse_when_valid_provider_then_command_is_credentials(self) -> None:
        parser = create_parser()
        args = parser.parse_args(["proxy", "credentials", "set", "digitalocean"])
        assert args.command == "credentials"

    def test_parse_when_valid_provider_then_credentials_command_is_set(self) -> None:
        parser = create_parser()
        args = parser.parse_args(["proxy", "credentials", "set", "digitalocean"])
        assert args.credentials_command == "set"

    def test_parse_when_valid_provider_then_provider_captured(self) -> None:
        parser = create_parser()
        args = parser.parse_args(["proxy", "credentials", "set", "digitalocean"])
        assert args.provider == "digitalocean"


class TestProxyCredentialsCheckParser:
    """``jerry proxy credentials check <provider>`` parses correctly."""

    def test_parse_when_valid_provider_then_credentials_command_is_check(self) -> None:
        parser = create_parser()
        args = parser.parse_args(["proxy", "credentials", "check", "digitalocean"])
        assert args.namespace == "proxy"
        assert args.command == "credentials"
        assert args.credentials_command == "check"
        assert args.provider == "digitalocean"


class TestProxyCredentialsDeleteParser:
    """``jerry proxy credentials delete <provider>`` parses correctly."""

    def test_parse_when_valid_provider_then_credentials_command_is_delete(self) -> None:
        parser = create_parser()
        args = parser.parse_args(["proxy", "credentials", "delete", "digitalocean"])
        assert args.namespace == "proxy"
        assert args.command == "credentials"
        assert args.credentials_command == "delete"
        assert args.provider == "digitalocean"


class TestProxyEngageParser:
    """``jerry proxy engage <config>`` parses correctly."""

    def test_parse_when_config_path_then_args_populated(self) -> None:
        parser = create_parser()
        args = parser.parse_args(["proxy", "engage", "/path/to/config.yaml"])
        assert args.namespace == "proxy"
        assert args.command == "engage"
        assert args.config == "/path/to/config.yaml"

    def test_parse_when_full_pipeline_flag_then_flag_true(self) -> None:
        parser = create_parser()
        args = parser.parse_args(["proxy", "engage", "/path/to/config.yaml", "--full-pipeline"])
        assert args.full_pipeline is True

    def test_parse_when_no_full_pipeline_flag_then_flag_false(self) -> None:
        parser = create_parser()
        args = parser.parse_args(["proxy", "engage", "/path/to/config.yaml"])
        assert args.full_pipeline is False


class TestProxyStatusParser:
    """``jerry proxy status --engagement <id>`` parses correctly."""

    def test_parse_when_engagement_id_then_args_populated(self) -> None:
        parser = create_parser()
        args = parser.parse_args(["proxy", "status", "--engagement", "RED-0001"])
        assert args.namespace == "proxy"
        assert args.command == "status"
        assert args.engagement == "RED-0001"


class TestProxyDestroyParser:
    """``jerry proxy destroy --engagement <id>`` parses correctly."""

    def test_parse_when_engagement_id_then_args_populated(self) -> None:
        parser = create_parser()
        args = parser.parse_args(["proxy", "destroy", "--engagement", "RED-0001"])
        assert args.namespace == "proxy"
        assert args.command == "destroy"
        assert args.engagement == "RED-0001"

    def test_parse_when_node_ids_then_ids_captured(self) -> None:
        parser = create_parser()
        args = parser.parse_args(
            ["proxy", "destroy", "--engagement", "RED-0001", "--node-ids", "n1", "n2"]
        )
        assert args.node_ids == ["n1", "n2"]

    def test_parse_when_no_node_ids_then_none(self) -> None:
        parser = create_parser()
        args = parser.parse_args(["proxy", "destroy", "--engagement", "RED-0001"])
        assert args.node_ids is None


class TestProxyGcParser:
    """``jerry proxy gc --engagement <id>`` parses correctly."""

    def test_parse_when_dry_run_then_dry_run_true(self) -> None:
        parser = create_parser()
        args = parser.parse_args(["proxy", "gc", "--engagement", "RED-0001", "--dry-run"])
        assert args.namespace == "proxy"
        assert args.command == "gc"
        assert args.engagement == "RED-0001"
        assert args.dry_run is True

    def test_parse_when_confirm_then_confirm_true(self) -> None:
        parser = create_parser()
        args = parser.parse_args(["proxy", "gc", "--engagement", "RED-0001", "--confirm"])
        assert args.confirm is True

    def test_parse_when_default_then_dry_run_true(self) -> None:
        """GC defaults to dry-run for safety."""
        parser = create_parser()
        args = parser.parse_args(["proxy", "gc", "--engagement", "RED-0001"])
        assert args.dry_run is True
        assert args.confirm is False


# ---------------------------------------------------------------------------
# Handler tests: ``_handle_proxy()`` routes correctly
# ---------------------------------------------------------------------------


class TestHandleProxyCredentialsSet:
    """Handler for ``jerry proxy credentials set`` stores key via getpass."""

    def test_handle_when_valid_key_then_stores_and_exits_zero(self) -> None:
        from src.interface.cli.main import _handle_proxy

        parser = create_parser()
        args = parser.parse_args(["proxy", "credentials", "set", "digitalocean"])

        with (
            patch("getpass.getpass", return_value="test-api-key-123"),
            patch(
                "src.proxy_infra.interface.cli.proxy_commands.credentials_set_command"
            ) as mock_set,
        ):
            exit_code = _handle_proxy(args, json_output=False)

        assert exit_code == 0
        mock_set.assert_called_once_with("digitalocean", "test-api-key-123")

    def test_handle_when_empty_key_then_exits_one(self) -> None:
        from src.interface.cli.main import _handle_proxy

        parser = create_parser()
        args = parser.parse_args(["proxy", "credentials", "set", "digitalocean"])

        with patch("getpass.getpass", return_value=""):
            exit_code = _handle_proxy(args, json_output=False)

        assert exit_code == 1


class TestHandleProxyCredentialsCheck:
    """Handler for ``jerry proxy credentials check`` reports presence."""

    def test_handle_when_found_then_exits_zero(self) -> None:
        from src.interface.cli.main import _handle_proxy

        parser = create_parser()
        args = parser.parse_args(["proxy", "credentials", "check", "digitalocean"])

        mock_result = MagicMock(found=True, provider="digitalocean", source="keychain")
        with patch(
            "src.proxy_infra.interface.cli.proxy_commands.credentials_check_command",
            return_value=mock_result,
        ):
            exit_code = _handle_proxy(args, json_output=False)

        assert exit_code == 0

    def test_handle_when_not_found_then_exits_one(self) -> None:
        from src.interface.cli.main import _handle_proxy

        parser = create_parser()
        args = parser.parse_args(["proxy", "credentials", "check", "digitalocean"])

        mock_result = MagicMock(found=False, provider="digitalocean", source="none")
        with patch(
            "src.proxy_infra.interface.cli.proxy_commands.credentials_check_command",
            return_value=mock_result,
        ):
            exit_code = _handle_proxy(args, json_output=False)

        assert exit_code == 1

    def test_handle_when_json_output_then_returns_json(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        from src.interface.cli.main import _handle_proxy

        parser = create_parser()
        args = parser.parse_args(["proxy", "credentials", "check", "digitalocean"])

        mock_result = MagicMock(found=True, provider="digitalocean", source="keychain")
        with patch(
            "src.proxy_infra.interface.cli.proxy_commands.credentials_check_command",
            return_value=mock_result,
        ):
            exit_code = _handle_proxy(args, json_output=True)

        assert exit_code == 0
        import json

        output = json.loads(capsys.readouterr().out)
        assert output["found"] is True
        assert output["provider"] == "digitalocean"
        assert output["source"] == "keychain"


class TestHandleProxyCredentialsDelete:
    """Handler for ``jerry proxy credentials delete`` removes credential."""

    def test_handle_when_deleted_then_exits_zero(self) -> None:
        from src.interface.cli.main import _handle_proxy

        parser = create_parser()
        args = parser.parse_args(["proxy", "credentials", "delete", "digitalocean"])

        with patch(
            "src.proxy_infra.interface.cli.proxy_commands.credentials_delete_command",
            return_value=True,
        ):
            exit_code = _handle_proxy(args, json_output=False)

        assert exit_code == 0

    def test_handle_when_not_found_then_exits_one(self) -> None:
        from src.interface.cli.main import _handle_proxy

        parser = create_parser()
        args = parser.parse_args(["proxy", "credentials", "delete", "digitalocean"])

        with patch(
            "src.proxy_infra.interface.cli.proxy_commands.credentials_delete_command",
            return_value=False,
        ):
            exit_code = _handle_proxy(args, json_output=False)

        assert exit_code == 1


class TestHandleProxyNoCommand:
    """Handler prints help when no subcommand given."""

    def test_handle_when_no_command_then_exits_one(self) -> None:
        from src.interface.cli.main import _handle_proxy

        parser = create_parser()
        args = parser.parse_args(["proxy"])
        exit_code = _handle_proxy(args, json_output=False)
        assert exit_code == 1


class TestHandleProxyStatus:
    """Handler for ``jerry proxy status`` lists nodes."""

    def test_handle_when_engagement_then_returns_nodes(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        from src.interface.cli.main import _handle_proxy

        parser = create_parser()
        args = parser.parse_args(["proxy", "status", "--engagement", "RED-0001"])

        mock_nodes = [
            MagicMock(id="node-1", ip="1.2.3.4", region="nyc3", status=MagicMock(value="active")),
        ]
        with (
            patch(
                "src.proxy_infra.interface.cli.proxy_commands.status_command",
                return_value=mock_nodes,
            ),
            patch(
                "src.interface.cli.main._create_proxy_adapter",
                return_value=(MagicMock(), MagicMock()),
            ) as _,
        ):
            exit_code = _handle_proxy(args, json_output=False)

        assert exit_code == 0

    def test_handle_when_raw_engagement_id_then_derives_tag(self) -> None:
        """User passes 'RED-0001', domain receives 'jerry-red-0001'."""
        from src.interface.cli.main import _handle_proxy

        parser = create_parser()
        args = parser.parse_args(["proxy", "status", "--engagement", "RED-0001"])

        with (
            patch(
                "src.proxy_infra.interface.cli.proxy_commands.status_command",
                return_value=[],
            ) as mock_status,  # noqa: F841
            patch(
                "src.interface.cli.main._create_proxy_adapter",
                return_value=(MagicMock(), MagicMock()),
            ) as _,
        ):
            _handle_proxy(args, json_output=False)

        # First arg to status_command is the engagement tag
        actual_tag = mock_status.call_args[0][0]
        assert actual_tag == "jerry-red-0001"


class TestHandleProxyDestroy:
    """Handler for ``jerry proxy destroy`` tears down infrastructure."""

    def test_handle_when_engagement_then_destroys_and_exits_zero(self) -> None:
        from src.interface.cli.main import _handle_proxy

        parser = create_parser()
        args = parser.parse_args(["proxy", "destroy", "--engagement", "RED-0001"])

        mock_result = MagicMock(is_all_successful=True, destroyed=["node-1"], failed=[])
        with (
            patch(
                "src.proxy_infra.interface.cli.proxy_commands.destroy_command",
                return_value=mock_result,
            ),
            patch(
                "src.interface.cli.main._create_proxy_adapter",
                return_value=(MagicMock(), MagicMock()),
            ) as _,
        ):
            exit_code = _handle_proxy(args, json_output=False)

        assert exit_code == 0

    def test_handle_when_raw_engagement_id_then_derives_tag(self) -> None:
        """User passes 'RED-0001', domain receives 'jerry-red-0001'."""
        from src.interface.cli.main import _handle_proxy

        parser = create_parser()
        args = parser.parse_args(["proxy", "destroy", "--engagement", "RED-0001"])

        mock_result = MagicMock(is_all_successful=True, destroyed=[], failed=[])
        with (
            patch(
                "src.proxy_infra.interface.cli.proxy_commands.destroy_command",
                return_value=mock_result,
            ) as mock_destroy,
            patch(
                "src.interface.cli.main._create_proxy_adapter",
                return_value=(MagicMock(), MagicMock()),
            ) as _,
        ):
            _handle_proxy(args, json_output=False)

        actual_tag = mock_destroy.call_args[0][0]
        assert actual_tag == "jerry-red-0001"


class TestHandleProxyGc:
    """Handler for ``jerry proxy gc`` garbage collects orphaned nodes."""

    def test_handle_when_dry_run_then_lists_orphans(self) -> None:
        from src.interface.cli.main import _handle_proxy

        parser = create_parser()
        args = parser.parse_args(["proxy", "gc", "--engagement", "RED-0001", "--dry-run"])

        with (
            patch(
                "src.proxy_infra.interface.cli.proxy_commands.gc_command",
                return_value=["orphan-1", "orphan-2"],
            ),
            patch(
                "src.interface.cli.main._create_proxy_adapter",
                return_value=(MagicMock(), MagicMock()),
            ) as _,
        ):
            exit_code = _handle_proxy(args, json_output=False)

        assert exit_code == 0

    def test_handle_when_confirm_then_destroys_orphans(self) -> None:
        from src.interface.cli.main import _handle_proxy

        parser = create_parser()
        args = parser.parse_args(["proxy", "gc", "--engagement", "RED-0001", "--confirm"])

        with (
            patch(
                "src.proxy_infra.interface.cli.proxy_commands.gc_command",
                return_value=["orphan-1"],
            ),
            patch(
                "src.interface.cli.main._create_proxy_adapter",
                return_value=(MagicMock(), MagicMock()),
            ) as _,
        ):
            exit_code = _handle_proxy(args, json_output=False)

        assert exit_code == 0

    def test_handle_when_raw_engagement_id_then_derives_tag(self) -> None:
        """User passes 'RED-0001', domain receives 'jerry-red-0001'."""
        from src.interface.cli.main import _handle_proxy

        parser = create_parser()
        args = parser.parse_args(["proxy", "gc", "--engagement", "RED-0001", "--dry-run"])

        with (
            patch(
                "src.proxy_infra.interface.cli.proxy_commands.gc_command",
                return_value=[],
            ) as mock_gc,
            patch(
                "src.interface.cli.main._create_proxy_adapter",
                return_value=(MagicMock(), MagicMock()),
            ) as _,
        ):
            _handle_proxy(args, json_output=False)

        actual_tag = mock_gc.call_args[0][0]
        assert actual_tag == "jerry-red-0001"


# ---------------------------------------------------------------------------
# main() routing test: ``proxy`` dispatched to ``_handle_proxy()``
# ---------------------------------------------------------------------------


class TestMainProxyRouting:
    """main() dispatches ``proxy`` namespace to ``_handle_proxy``."""

    def test_main_when_proxy_namespace_then_routes_to_handler(self) -> None:
        import importlib

        main_module = importlib.import_module("src.interface.cli.main")

        with (
            patch.object(main_module, "_handle_proxy", return_value=0) as mock_handler,
            patch("sys.argv", ["jerry", "proxy", "credentials", "check", "digitalocean"]),
        ):
            exit_code = main_module.main()

        assert exit_code == 0
        mock_handler.assert_called_once()
