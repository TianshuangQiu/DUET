import streamlit as st
from streamlit_sortables import sort_items
import json
from copy import deepcopy
from duet.visualize.visualizer import Motifs, Visualizer
import pdb

with open("config/motifs.json", "r") as r:
    MOTIF_LIST = json.load(r)

if "phase" not in st.session_state:
    st.session_state["phase"] = 0

if "modifying" not in st.session_state:
    st.session_state["modifying"] = False

if "motif_func" not in st.session_state:
    st.session_state["motif_func"] = Motifs()

if "visualizer" not in st.session_state:
    st.session_state["visualizer"] = Visualizer()


def motif_variation(container: st.container, config: dict, name, key):
    modified_name = container.text_input("Name", name, key=f"{key}_txt")

    if "type" in config:
        t_idx = list(MOTIF_LIST.keys()).index(config["type"])
    else:
        t_idx = 0
    motif_type = container.selectbox(
        f"Type:",
        MOTIF_LIST.keys(),
        index=t_idx,
        key=f"{key}_select",
    )
    config["type"] = motif_type

    parameters = MOTIF_LIST[motif_type]["params"]
    if "params" not in config:
        config["params"] = {}
    for i, (k, v) in enumerate(parameters.items()):
        value = container.slider(k, v[0], v[1], key=f"{key}_param_{i}")
        config["params"][f"{k}"] = value

    return modified_name, config


if not st.session_state["modifying"]:
    with st.sidebar:
        st.markdown("# DUET")
        st.markdown("### 0. Select configuration")
        zero = st.button("Select", key=0)
        st.markdown("### 1. View and modify Current configuration")
        one = st.button("View", key=1)
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
            st.session_state["config"], st.session_state["ordering"] = json.load(file)
            st.session_state["phase"] = 1
            st.experimental_rerun()
        if make_new:
            st.session_state["config"] = {}
            st.session_state["ordering"] = []
            st.session_state["phase"] = 1
            st.experimental_rerun()

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
                st.experimental_rerun()
        edit = st.button("edit motif")
        if edit:
            if len(st.session_state["ordering"]) <= 1:
                st.warning("Please insert more items first")
            else:
                st.session_state["modifying"] = True
                st.experimental_rerun()
        remove = st.button("remove last motif")
        if remove:
            rm_conf = st.session_state["ordering"].pop(-1)
            st.session_state["config"].pop(rm_conf)
            st.experimental_rerun()
    elif st.session_state["phase"] == 2:
        st.markdown("### Select range for visualization")
        vis_range = st.slider(
            "Index of motifs",
            0,
            len(st.session_state["config"]) - 1,
            value=(0, len(st.session_state["config"]) - 1),
        )
        st.markdown(
            f"#### {st.session_state['ordering'][vis_range[0]]} \
            :::: {st.session_state['ordering'][vis_range[1]]}"
        )
        render = st.button("Create Visualization")

        if render:
            motif_names = st.session_state["ordering"][vis_range[0] : vis_range[1] + 1]
            out_config = []

            traj_creator = Motifs()
            trajectory = []
            for m in motif_names:
                param_dict = st.session_state["config"][m]
                func = getattr(traj_creator, param_dict["type"])
                trajectory.extend(func(param_dict["params"]))
            st.markdown("### Generated trajectory:")
            st.write(trajectory)
            st.session_state["visualizer_figs"] = st.session_state[
                "visualizer"
            ].visualize(trajectory)

        visualizer_figs = st.session_state.get("visualizer_figs", [None, None])
        frame = st.slider("Frame", 0, len(visualizer_figs) - 1)
        if visualizer_figs[frame] is not None:
            st.plotly_chart(visualizer_figs[frame])
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
        st.experimental_rerun()
    if revert:
        st.session_state["modifying"] = False
        st.session_state["config"], st.session_state["ordering"] = st.session_state.pop(
            "backup"
        )
        st.experimental_rerun()

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
