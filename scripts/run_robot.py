from duet.execute.motifs import *
import json
import streamlit as st
from streamlit_sortables import sort_items
from copy import deepcopy
import numpy as np
import cowsay
import pdb


if "phase" not in st.session_state:
    st.session_state["phase"] = 0

if "modifying" not in st.session_state:
    st.session_state["modifying"] = False

if "motif_func" not in st.session_state or "motifs" not in st.session_state:
    with open("config/robot_ready.json", "r") as r:
        RBT_MOTIFS = json.load(r)
    MOTIF_FUNCS = {}
    for k in RBT_MOTIFS.keys():
        MOTIF_FUNCS[k] = locals()[k]
    st.session_state["motif_func"] = MOTIF_FUNCS
    st.session_state["motif_dict"] = RBT_MOTIFS
else:
    MOTIF_FUNCS = st.session_state["motif_func"]
    RBT_MOTIFS = st.session_state["motif_dict"]


def motif_variation(container: st.container, config: dict, name, key):
    modified_name = container.text_input("Name", name, key=f"{key}_txt")
    if "type" in config:
        t_idx = list(RBT_MOTIFS.keys()).index(config["type"])
    else:
        t_idx = 0
    motif_type = container.selectbox(
        f"Type:",
        RBT_MOTIFS.keys(),
        index=t_idx,
        key=f"{key}_select",
    )
    config["type"] = motif_type

    if "params" in RBT_MOTIFS[motif_type]:
        parameters = RBT_MOTIFS[motif_type]["params"]
        if "params" not in config:
            config["params"] = {}
        for i, (k, v) in enumerate(parameters.items()):
            value = container.slider(k, v[0], v[1], key=f"{key}_param_{i}")
            config["params"][k] = value
    else:
        container.write("No editable parameters for this motif")

    return modified_name, config


if not st.session_state["modifying"]:
    with st.sidebar:
        st.markdown("# DUET")
        st.markdown("### 0. Select configuration")
        zero = st.button("Select", key=0)
        st.markdown("### 1. View and modify Current configuration")
        one = st.button("View", key=1)
        st.markdown("### 2. Compute Trajectory")
        two = st.button("Compute", key=2)

    if zero:
        st.session_state["phase"] = 0
    if one:
        st.session_state["phase"] = 1
    if two:
        st.session_state["phase"] = 2

    if st.session_state["phase"] == 0:
        file = st.file_uploader("Upload saved config file")
        upload = st.button("Upload")
        make_new = st.button("Create new configuration instead")

        if upload:
            st.session_state["config"], st.session_state["ordering"] = json.load(file)
            st.session_state["phase"] = 1
            st.rerun()
        if make_new:
            st.session_state["config"] = {}
            st.session_state["ordering"] = []
            st.session_state["phase"] = 1
            st.rerun()

    elif st.session_state["phase"] == 1:
        all_sections = list(st.session_state["config"].keys())
        if "ordering" not in st.session_state:
            st.session_state["ordering"] = sort_items(all_sections)
        else:
            st.session_state["ordering"] = sort_items(st.session_state["ordering"])
        new_motif_name = st.text_input("Name for new section", value="filler_name")
        add = st.button("add motif")
        if add:
            if new_motif_name in st.session_state["config"]:
                st.warning("Name already exists in sequence!")
            else:
                st.session_state["config"][new_motif_name] = {}
                st.session_state["ordering"].append(new_motif_name)
                st.rerun()
        edit = st.button("edit motif")
        if edit:
            if len(st.session_state["ordering"]) <= 1:
                st.warning("Please insert more items first")
            else:
                st.session_state["modifying"] = True
                st.rerun()
        remove = st.button("remove last motif")
        if remove:
            rm_conf = st.session_state["ordering"].pop(-1)
            st.session_state["config"].pop(rm_conf)
            st.rerun()
    elif st.session_state["phase"] == 2:
        # Computing trajectory
        robot_ready_funcs = []
        for o in st.session_state["ordering"]:
            curr_config_dict: dict = st.session_state["config"][o]
            kwargs = curr_config_dict.get("params", {})
            func = st.session_state["motif_func"][st.session_state["config"][o]["type"]]
            robot_ready_funcs.append(func(**kwargs))
        st.markdown("### Trajectory Computed")
        if "robot" not in st.session_state:
            connect = st.button("Connect to Robot")
            if connect:
                st.session_state["robot"] = UR5Robot(gripper=True)
            robot = None
        else:
            st.write("Connected to UR5")
            robot: UR5Robot = st.session_state["robot"]

        execute = st.button("Execute")

        if execute:
            for h in robot_ready_funcs:
                h(robot)
        save_file_name = st.text_input("Save Name", "tmp_save.json")
        save = st.button("Save Configuration")

        if save:
            with open(f"save/{save_file_name}", "w") as w:
                json.dump((st.session_state["config"], st.session_state["ordering"]), w)

else:
    if "backup" not in st.session_state:
        st.session_state["backup"] = (
            deepcopy(st.session_state["config"]),
            deepcopy(st.session_state["ordering"]),
        )
    with st.sidebar:
        st.markdown("# DUET")
        idx = st.slider(
            "Index of motif to change", 0, len(st.session_state["config"]) - 1, 0
        )
        commit = st.button("Commit changes")
        revert = st.button("Discard changes")
    if commit:
        st.session_state["modifying"] = False
        st.session_state.pop("backup")
        st.rerun()
    if revert:
        st.session_state["modifying"] = False
        st.session_state["config"], st.session_state["ordering"] = st.session_state.pop(
            "backup"
        )
        st.rerun()

    current_config_name = st.session_state["ordering"][idx]
    st.markdown(f"### Editing Motif")
    motif_container = st.container()
    name, current_varation = motif_variation(
        motif_container,
        st.session_state["config"].pop(current_config_name),
        name=current_config_name,
        key="mot",
    )
    st.session_state["ordering"][idx] = name
    st.session_state["config"][name] = current_varation
