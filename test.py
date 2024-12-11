import omni.replicator.core as rep

with rep.new_layer("randomizer"):
    object_group = rep.get.prim_at_path(path="/World/Cube")
    with rep.trigger.on_frame(max_execs=60):
        with object_group:
            mod = rep.modify.pose(
                position=rep.distribution.uniform((-500., -500., -500.), (500., 500., 500.))
            )

with rep.new_layer("Camera"):
    camera = rep.create.camera()
    render_product = rep.create.render_product(camera, (1920, 1080))

with rep.new_layer("Writer"):
    writer = rep.writers.get("BasicWriter")
    writer.initialize(output_dir="C:/Users/ryan0511/Downloads/test_replicator/", rgb=True)
    writer.attach(render_product)
rep.orchestrator.run()

# =================================================================================================

import omni.replicator.core as rep

with rep.new_layer():
	camera = rep.create.camera()
	render_product = rep.create.render_product(camera, (1920, 1080))

	writer = rep.writers.get("BasicWriter")
	writer.initialize(output_dir = "C:/Users/ryan0511/Downloads/test_replicator/", rgb = True)
	writer.attach(render_product)

	object_group = rep.get.prim_at_path (path = "/World/Cube")

	with rep.trigger.on_frame(max_execs=30):
	   with object_group:
	       mod = rep.modify.pose(position=rep.distribution.uniform((-500., -500., -500.), (500., 500., 500.)))
rep.orchestrator.run()
