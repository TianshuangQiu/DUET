import streamlit as st
import json
from duet.visualize.visualizer import Motifs
import pdb

with open("config/motifs.json", "r") as r:
    MOTIF_LIST = json.load(r)

if "phase" not in st.session_state:
    st.session_state["phase"] = 0

if "modifying" not in st.session_state:
    st.session_state["modifying"] = False

if "motif_func" not in st.session_state:
    st.session_state["motif_func"] = Motifs()


def motif_variation(container: st.container, config: dict, key):
    name = container.text_input("Name", config.get("name", ""), key=f"{key}_txt")
    config["name"] = name

    if "type" in config:
        t_idx = list(MOTIF_LIST.keys()).index(config["type"])
    else:
        t_idx = 0
    motif_type = st.selectbox(
        f"Type:",
        MOTIF_LIST.keys(),
        index=t_idx,
        key=f"{key}_select",
    )
    config["type"] = motif_type

    index = container.slider(
        "Position in queue",
        0,
        len(st.session_state["config"]),
        config.get("index", len(st.session_state["config"])),
        key=f"{key}_idx",
    )
    config["index"] = index

    parameters = MOTIF_LIST[motif_type]["params"]
    if "params" not in config:
        config["params"] = {}
    for i, (k, v) in enumerate(parameters.items()):
        value = container.slider(k, v[0], v[1], key=f"{key}_param_{i}")
        config["params"][f"{k}"] = value

    return config


if not st.session_state["modifying"]:
    with st.sidebar:
        st.markdown("### 0. Select configuration")
        zero = st.button("Select", key=0)
        st.markdown("### 1. Modify configuration")
        one = st.button("Modify", key=1)
        save_modification = st.button("Save")
        st.markdown("### 2. Create visualization")
        two = st.button("Create", key=2)

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
            st.session_state["config"] = json.load(upload)
            st.session_state["phase"] = 1
            st.experimental_rerun()
        if make_new:
            st.session_state["config"] = [{}]
            st.session_state["phase"] = 1
            st.experimental_rerun()
    elif st.session_state["phase"] == 1:
        all_containers = []
        for i, c in enumerate(st.session_state["config"]):
            st.markdown(f"### Motif {i}")
            cont = st.container()
            st.session_state["config"][i] = motif_variation(cont, c, key=f"mot_{i}")
            all_containers.append(cont)

        st.session_state["config"] = sorted(
            st.session_state["config"], key=lambda x: x["index"]
        )

        add = st.button("add motif")
        if add:
            st.session_state["config"].append({})
            st.experimental_rerun()
    elif st.session_state["phase"] == 2:
        st.markdown("### Select range for visualization")
        vis_range = st.slider(
            "Index of motifs",
            0,
            len(st.session_state["config"]),
            value=(0, len(st.session_state["config"])),
        )
        render = st.button("Create Visualization")
        save = st.button("Save Visualization")

else:
    with st.sidebar:
        st.slider()
